############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set,Tuple
from json import load
############ INSTALLED IMPORTS ###########################
from pandas import read_json
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import cosine_similarity_for_sets
##########################################################
class QuranAudio:
    def __init__(self) -> None:
        self.URL = "https://raw.githubusercontent.com/mohammedterryjack/quran/master/"
        self.PATH = "data/audio"
        self.AUDIO_FORMAT = "mp3"
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

    def local_filename(self, verse_name:str, reciter:int) -> str:
        """ get local filename for verse audio """
        FILENAME = self._filename(verse_name=verse_name, reciter=reciter)
        return f"{self.PATH}/{FILENAME}.{self.AUDIO_FORMAT}"

    def url(self, verse_name:str, reciter:int) -> str:
        """ get local filename for verse audio """
        PATH_AND_FILENAME = self.local_filename(verse_name=verse_name, reciter=reciter)
        return f"{self.URL}/{PATH_AND_FILENAME}?raw=true"

class QuranText:
    def __init__(self) -> None:
        self.CROSS_REFERENCES = read_json("data/mushaf/quran.json")
        self.ENGLISH = read_json("data/mushaf/quran_en.json")
        self.ARABIC = read_json("data/mushaf/quran_ar.json")
        with open("data/mushaf/quran_features.json") as json_file:
            self.FEATURES = load(json_file)
        self.VERSE_NAMES = list(self.ENGLISH.keys())
        self.CHAPTER_NAMES = self._get_surah_names()

    def next_verse(self, verse:str) -> str:  
        return self._increase_verse_by_n(verse=verse,n=1)

    def previous_verse(self, verse:str) -> str:  
        return self._increase_verse_by_n(verse=verse,n=-1)

    def _increase_verse_by_n(self, verse:str,n:int) -> str:
        verse_index = self.VERSE_NAMES.index(verse)
        verse_index += n
        verse_index %= len(self.VERSE_NAMES)
        return self.VERSE_NAMES[verse_index]

    def _get_surah_names(self) -> List[str]:
        surah_names = []
        for index in range(1,115):
            with open(f"raw_data/quran_surah_names/surah_{index}.json", encoding='utf-8') as json_file:
                surah_names.append(load(json_file)["name"])
        return surah_names

    def semantic_features_for_verse(self, verse:str) -> Set[str]:
        index = str(self.VERSE_NAMES.index(verse))
        return set(self.FEATURES[index])

    def _semantic_features(self) -> Iterable[Set[str]]:
        for features in self.FEATURES.values():
            yield set(features)
        
    def arabic_verse(self,verse:str) -> str:
        return self.ARABIC[verse]["ARABIC"]

    def english_translations_of_verse(self,verse:str) -> List[str]:
        return self.ENGLISH[verse]["ENGLISH"][:-1]

    def english_translation_of_verse(self,verse:str,translator:int=8) -> str:
        return self.ENGLISH[verse]["ENGLISH"][max(min(translator,17),0)]

    def similar_verses_to_verse(self,verse:str, top_n:int=3) -> List[str]:
        return self.CROSS_REFERENCES[verse][:max(min(top_n,10),0)]

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
        return f"{self.URL}/t{self.BOOKS.get(f'{cannon}/{book}')}{str(chapter).zfill(2)}.{self.AUDIO_FORMAT}"

class BibleText(Bible):
    def __init__(self) -> None:
        super().__init__() 
        self.PATH = "data/tanakh/{directory}/{book}_{language_code}.json"
        self.ENGLISH = self._load(language_code="en")
        self.HEBREW = self._load(language_code="he")

    def _load(self, language_code:str) -> dict:
        bible = {}
        for book_name in self.BOOKS:
            directory,book = book_name.lower().split("/")
            if directory not in bible:
                bible[directory] = {}
            path = self.PATH.format(
                directory=directory,
                book=book,
                language_code=language_code
            )
            with open(path,encoding='utf-8') as json_file:
                bible[directory][book] = load(json_file)["text"]
        return bible 

    def verse(self, language_code:str, cannon:str, book:str, chapter:int, verse:int) -> str:
        version = (self.HEBREW,self.ENGLISH)[int(language_code=="en")]
        return version[cannon][book][chapter-1][verse-1] 

