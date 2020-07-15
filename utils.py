############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set
from ujson import load
############ INSTALLED IMPORTS ###########################
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import cosine_similarity_for_sets
##########################################################
class QuranAudio:
    def __init__(self) -> None:
        self.URL = "https://raw.githubusercontent.com/mohammedterryjack/quran-data/master/audio/{filename}.mp3?raw=true"
        self.WARSH_FILES = "warsh_aljazari"
        self.HAFS_FILES = "hafs_alafasy"

    def _filename(self, verse_name:str, reciter:int) -> str:
        """ get name of audio file for verse """
        RECITER = (
            self.HAFS_FILES, 
            self.WARSH_FILES
        )[min(max(reciter,0),1)]
        try:
            chapter,verse = verse_name.split(":")
            VERSE_NAME = f"{chapter.zfill(3)}{verse.zfill(3)}"
        except:
            VERSE_NAME = "audhubillah"
        return f"{RECITER}/{VERSE_NAME}"

    def url(self, verse_name:str, reciter:int) -> str:
        """ get local filename for verse audio """
        return self.URL.format(
            filename=self._filename(verse_name=verse_name, reciter=reciter)
        )

class HolyScripture:
    def __init__(self,scripture_name:str) -> None:
        self.NAME = scripture_name
        with open(f"data/{self.NAME}/metadata.json") as json_file:          
            self._METADATA = load(json_file)
        with open(f"html_templates/{self.NAME}_verse.html") as html_file:
            self.HTML = html_file.read()
        self.VERSE_NAMES = self._METADATA["VERSE_NAMES"]

    def get_next_verse_name(self,verse_name:str) -> str:  
        return self._increase_verse_by_n(verse=verse_name,n=1)

    def get_previous_verse_name(self,verse_name:str) -> str:  
        return self._increase_verse_by_n(verse=verse_name,n=-1)
    
    def _increase_verse_by_n(self, verse:str,n:int) -> str:
        verse_index = self.VERSE_NAMES.index(verse)
        verse_index += n
        verse_index %= len(self.VERSE_NAMES)
        return self.VERSE_NAMES[verse_index]
    
    @staticmethod
    def get_features(verse_json:dict) -> Set[str]:
        return set(verse_json["FEATURES"])


class Quran(HolyScripture):
    def __init__(self) -> None:
        super().__init__(scripture_name="quran")    
        self.DEFAULT_TRANSLATOR = 6
        self.CHAPTER_NAMES = self._METADATA["CHAPTER_NAMES"]
        with open("html_templates/quran_verse.html") as html_file:
            self.HTML = html_file.read()
        self.AUDIO = QuranAudio()
    
    @staticmethod
    def get_english_parallel(verse_json:dict) -> str:
        return list(verse_json["ENGLISH"].values())[:-1]

    @staticmethod
    def get_english(verse_json:dict,translator:int) -> str:
        return verse_json["ENGLISH"][f"TRANSLATION_{max(min(translator,17),0)}"]

    @staticmethod
    def get_arabic(verse_json:dict) -> str:
        return verse_json["ARABIC"]

    @staticmethod
    def get_crossreference_bible(verse_json:dict,top_n:int=3) -> List[str]:
        return verse_json["CROSS_REFERENCE"]["BIBLE"][:max(min(top_n,10),0)]

    @staticmethod
    def get_crossreference_quran(verse_json:dict,top_n:int=3) -> List[str]:
        return verse_json["CROSS_REFERENCE"]["QURAN"][:max(min(top_n,10),0)]
        
    def get_chapter_name(self,chapter_index:str) -> str:
        return self.CHAPTER_NAMES[int(chapter_index)-1]

    def get_verse_json(self,chapter:str,verse:str) -> dict:
        with open(f"data/{self.NAME}/{chapter}/{verse}.json") as json_file:
            return load(json_file)

    def get_english_summary_via_verse_name(self,verse_name:str,summary_length:int=50) -> List[str]:
        return self.get_english(
            verse_json=self.get_verse_json(*verse_name.split(":")),
            translator=self.DEFAULT_TRANSLATOR  
        )[:summary_length]

    def get_all_features(self) -> Iterable[Set[str]]:
        for verse_name in self.VERSE_NAMES:
            yield self.get_features(
                verse_json = self.get_verse_json(*verse_name.split(":"))
            )

    def get_verse_names_relevant_to_query(self, query_features:Set[str],top_n:int=3) -> List[str]:
        semantic_scores = list(
            map(
                lambda verse_features: cosine_similarity_for_sets(
                    features_a=query_features,
                    features_b=verse_features
                ),
                self.get_all_features()
            )
        )
        verse_indexes = argsort(semantic_scores)[:-top_n-1:-1]
        return list(map(lambda index:self.VERSE_NAMES[index], verse_indexes))

    # def common_features(self, query_features:Set[str], verse:str) -> Set[str]:
    #     return query_features.intersection(
    #         self.semantic_features_for_verse(verse)
    #     )


BOOKS_IN_TANAKH = {
    "torah/genesis":"01","torah/exodus":"02","torah/leviticus":"03","torah/numbers":"04","torah/deuteronomy":"05",
    "prophets/joshua":"06","prophets/judges":"07","prophets/i%20samuel":"08a","prophets/ii%20samuel":"08b",
    "prophets/i%20kings":"09a","prophets/ii%20kings":"09b","prophets/isaiah":"10","prophets/jeremiah":"11",
    "prophets/ezekiel":"12","prophets/hosea":"13","prophets/joel":"14","prophets/amos":"15","prophets/obadiah":"16",
    "prophets/jonah":"17","prophets/micah":"18","prophets/nahum":"19","prophets/habakkuk":"20",
    "prophets/zephaniah":"21","prophets/haggai":"22","prophets/zechariah":"23","prophets/malachi":"24",
    "writings/i%20chronicles":"25a","writings/ii%20chronicles":"25b","writings/psalms":"26","writings/job":"27",
    "writings/proverbs":"28","writings/ruth":"29","writings/song%20of%20songs":"30","writings/ecclesiastes":"31",
    "writings/lamentations":"32","writings/esther":"33","writings/daniel":"34","writings/ezra":"35a","writings/nehemiah":"35b"
}


class TanakhAudio:
    def __init__(self) -> None:
        self.URL = "http://www.mechon-mamre.org/mp3"
        self.AUDIO_FORMAT = "mp3"
        self.BOOKS = BOOKS_IN_TANAKH

    def url(self, cannon:str, book:str, chapter:int) -> str:
        """ get url of audio file for book """
        chapter_key = str(chapter)
        if len(chapter_key) == 3:
            a,b,c = chapter_key
            chapter_key = f"{chr(int(a+b)+87)}{c}"
        else:
            chapter_key = chapter_key.zfill(2)
        return f"{self.URL}/t{self.BOOKS.get(f'{cannon}/{book}')}{chapter_key}.{self.AUDIO_FORMAT}"


class Tanakh(HolyScripture):
    def __init__(self) -> None:
        super().__init__(scripture_name="tanakh") 
        self.BOOKS = BOOKS_IN_TANAKH
        self.AUDIO = TanakhAudio()

    def get_verse_json(self,collection:str,book:str,chapter:str,verse:str) -> dict:
        with open(f"data/{self.NAME}/{collection}/{book.replace(' ','%20')}/{chapter}/{verse}.json") as json_file:
            return load(json_file)

    def get_english_summary_via_verse_name(self,verse_name:str,summary_length:int=50) -> List[str]:
        return self.get_english(
            verse_json=self.get_verse_json(*verse_name.split(":"))            
        )[:summary_length]

    @staticmethod
    def get_english(verse_json:dict) -> str:
        return verse_json["ENGLISH"]

    @staticmethod
    def get_hebrew(verse_json:dict) -> str:
        return verse_json["HEBREW"]

    def get_all_features(self) -> Iterable[Set[str]]:
        for verse_name in self.VERSE_NAMES:
            yield self.get_features(
                verse_json = self.get_verse_json(*verse_name.split(":"))
            )

    def get_verse_names_relevant_to_query(self, query_features:Set[str],top_n:int=3) -> List[str]:
        semantic_scores = list(
            map(
                lambda verse_features: cosine_similarity_for_sets(
                    features_a=query_features,
                    features_b=verse_features
                ),
                self.get_all_features()
            )
        )
        verse_indexes = argsort(semantic_scores)[:-top_n-1:-1]
        return list(map(lambda index:self.VERSE_NAMES[index], verse_indexes))