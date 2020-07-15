############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set
from json import load
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

class QuranText:
    def __init__(self) -> None:   
        with open("data/mushaf/metadata.json") as json_file:          
            METADATA = load(json_file)
        self.VERSE_NAMES = METADATA["VERSE_NAMES"]
        self.CHAPTER_NAMES = METADATA["CHAPTER_NAMES"]
    
    def get_verse_json(self,verse_name:str) -> dict:
        chapter,verse = verse_name.split(":")
        with open("data/mushaf/{chapter}/{verse}.json") as json_file:
            return load(json_file)
    
    def _increase_verse_by_n(self, verse:str,n:int) -> str:
        verse_index = self.VERSE_NAMES.index(verse)
        verse_index += n
        verse_index %= len(self.VERSE_NAMES)
        return self.VERSE_NAMES[verse_index]

    # def common_features(self, query_features:Set[str], verse:str) -> Set[str]:
    #     return query_features.intersection(
    #         self.semantic_features_for_verse(verse)
    #     )

    @staticmethod
    def get_english(verse_json:dict,translator:int) -> str:
        return verse_json["ENGLISH"][f"TRANSLATION_{max(min(translator,17),0)}"]

    @staticmethod
    def get_arabic(verse_json:dict) -> str:
        return verse_json["ARABIC"]

    @staticmethod
    def get_features(verse_json:dict) -> Set[str]:
        return set(verse_json["FEATURES"])

    @staticmethod
    def get_crossreference_bible(verse_json:dict,top_n:int=3) -> List[str]:
        return verse_json["CROSS_REFERENCE"]["BIBLE"][:max(min(top_n,10),0)]

    @staticmethod
    def get_crossreference_quran(verse_json:dict,top_n:int=3) -> List[str]:
        return verse_json["CROSS_REFERENCE"]["QURAN"][:max(min(top_n,10),0)]

    @staticmethod
    def get_next_verse_name(verse_name:str) -> str:  
        return QuranText._increase_verse_by_n(verse=verse_name,n=1)

    @staticmethod
    def get_previous_verse_name(verse_name:str) -> str:  
        return QuranText._increase_verse_by_n(verse=verse_name,n=-1)


    # def _semantic_features(self) -> Iterable[Set[str]]:
    #     for features in self.FEATURES().values():
    #         yield set(features)
        

    # def semantically_similar_verses_to_query(self,query_features:Set[str],top_n:int=3) -> List[str]:
    #     semantic_scores = list(
    #         map(
    #             lambda verse_features: cosine_similarity_for_sets(
    #                 features_a=query_features,
    #                 features_b=verse_features
    #             ),
    #             self._semantic_features()
    #         )
    #     )
    #     verse_indexes = argsort(semantic_scores)[:-top_n-1:-1]
    #     return list(map(lambda index:self.VERSE_NAMES[index], verse_indexes))


class Bible:
    def __init__(self) -> None:
        self.BOOKS = {
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


class BibleAudio(Bible):
    def __init__(self) -> None:
        super().__init__() 
        self.URL = "http://www.mechon-mamre.org/mp3"
        self.AUDIO_FORMAT = "mp3"

    def url(self, cannon:str, book:str, chapter:int) -> str:
        """ get url of audio file for book """
        chapter_key = str(chapter)
        if len(chapter_key) == 3:
            a,b,c = chapter_key
            chapter_key = f"{chr(int(a+b)+87)}{c}"
        else:
            chapter_key = chapter_key.zfill(2)
        return f"{self.URL}/t{self.BOOKS.get(f'{cannon}/{book}')}{chapter_key}.{self.AUDIO_FORMAT}"

class BibleText(Bible):
    def __init__(self) -> None:
        super().__init__() 
        self.PATH = "data/tanakh/{directory}/{book}_{language_code}.json"
        self.VERSE_NAMES = list(self._verse_names())

    def FEATURES(self) -> dict:
        return self._load_features()

    def ENGLISH(self) -> dict:
        return self._load(path=self.PATH,language_code="en",book_names=self.BOOKS)

    def HEBREW(self) -> dict:
        return self._load(path=self.PATH,language_code="he",book_names=self.BOOKS)

    @staticmethod
    def _load_features() -> dict:
         with open("data/tanakh/bible_features.json") as json_file:
            return load(json_file)

    @staticmethod
    def _load(path:str, language_code:str, book_names:List[str]) -> dict:
        bible = {}
        for book_name in book_names:
            directory,book = book_name.lower().split("/")
            if directory not in bible:
                bible[directory] = {}
            full_path = path.format(
                directory=directory,
                book=book,
                language_code=language_code
            )
            with open(full_path,encoding='utf-8') as json_file:
                bible[directory][book] = load(json_file)["text"]
        return bible 

    def next_verse(self, verse:str) -> str:  
        return self._increase_verse_by_n(verse=verse,n=1)

    def previous_verse(self, verse:str) -> str:  
        return self._increase_verse_by_n(verse=verse,n=-1)

    def _increase_verse_by_n(self, verse:str,n:int) -> str:
        verse_index = self.VERSE_NAMES.index(verse)
        verse_index += n
        verse_index %= len(self.VERSE_NAMES)
        return self.VERSE_NAMES[verse_index]

    def verse(self, language_code:str, cannon:str, book:str, chapter:int, verse:int) -> str:
        version = self.ENGLISH() if language_code=="en" else self.HEBREW()
        return version[cannon][book][chapter-1][verse-1] 


    def _semantic_features(self) -> Iterable[Set[str]]:
        for cannon,books in self.FEATURES().items():
            for book,chapters in books.items():
                for verses in chapters:
                    for verse_features in verses:
                        yield set(verse_features)

    def _verse_names(self) -> Iterable[str]:
        for cannon,books in self.FEATURES().items():
            for book,chapters in books.items():
                for chapter_index,verses in enumerate(chapters):
                    for verse_index,verse_features in enumerate(verses):
                        yield f"{cannon}:{book}:{chapter_index+1}:{verse_index+1}"

    def semantically_similar_verses_to_query(self,query_features:Set[str],top_n:int=3) -> List[str]:
        semantic_scores = list(
            map(
                lambda verse_features: cosine_similarity_for_sets(
                    features_a=query_features,
                    features_b=verse_features
                ),
                self._semantic_features()
            )
        )
        verse_indexes = argsort(semantic_scores)[:-top_n-1:-1]
        return list(map(lambda index:self.VERSE_NAMES[index], verse_indexes))
