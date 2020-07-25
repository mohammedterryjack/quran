############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set
from ujson import load,loads
from datetime import datetime
from urllib.request import urlopen 
############ INSTALLED IMPORTS ###########################
from numpy import argsort
############   LOCAL IMPORTS   ###########################
##########################################################
def cosine_similarity_for_sets(features_a:set, features_b:set) -> float: 
    """
    returns the cosine similarity of two sets
    1.0=Identical. 0.0=Nothing in Common
    """
    features_in_common = features_a.intersection(features_b)
    denominator = len(features_a)**.5 * len(features_b)**.5
    return len(features_in_common)/denominator if denominator else .0

class QuranAudio:
    def __init__(self) -> None:
        self.URL = "https://raw.githubusercontent.com/mohammedterryjack/quran-data/master/audio-quran/{filename}.mp3?raw=true"
        self.WARSH_FILES = "warsh_aljazari"
        self.HAFS_FILES = "hafs_alafasy"
        self.HAMZA_FILES = "hamza_nuh"

    def _filename(self, verse_name:str, reciter:int) -> str:
        """ get name of audio file for verse """
        RECITER = (
            self.HAFS_FILES, 
            self.WARSH_FILES,
            self.HAMZA_FILES,
        )[min(max(reciter,0),2)]
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
        self.URL = "https://raw.githubusercontent.com/mohammedterryjack/quran-data/master/{scripture}/{book_chapter_verse}.json"
        self.NAME = scripture_name
        with urlopen(self.URL.format(scripture = self.NAME, book_chapter_verse="metadata")) as url:
            self._METADATA = loads(url.read().decode())
        with open(f"html_templates/{self.NAME}_verse.html") as html_file:
            self.HTML = html_file.read()
        self.VERSE_NAMES = self._METADATA["VERSE_NAMES"]
        self.KEYWORDS = self._METADATA["KEYWORDS"]
        
    def verse_name_for_now(self) -> str:
        return self.VERSE_NAMES[self._index_for_now()]

    def _index_for_now(self) -> int:
        return HolyScripture._minutes_into_the_year() // self._update_every_n_minutes()

    def _update_every_n_minutes(self) -> int:
        return self._a_year_in_minutes() // len(self.VERSE_NAMES)

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

    @staticmethod
    def _a_year_in_minutes() -> int:
        YEAR_IN_DAYS = 365
        DAY_IN_HOURS = 24
        HOUR_IN_MINUTES = 60
        return YEAR_IN_DAYS * DAY_IN_HOURS * HOUR_IN_MINUTES
    
    @staticmethod
    def _minutes_into_the_year() -> int:
        SECONDS_IN_MINUTE = 60
        now = datetime.now()
        start_of_year = datetime(
            year=now.year,
            month=1,
            day=1
        )
        seconds_into_the_year = (now - start_of_year).total_seconds()
        return int(seconds_into_the_year // SECONDS_IN_MINUTE)



class Quran(HolyScripture):
    def __init__(self) -> None:
        super().__init__(scripture_name="quran")    
        self.DEFAULT_TRANSLATOR = 7
        self.CHAPTER_NAMES = self._METADATA["CHAPTER_NAMES"]
        with open("html_templates/quran_verse.html") as html_file:
            self.HTML = html_file.read()
        with open("html_templates/quran_verse_not_found.html") as html_file:
            self.HTML_ERROR = html_file.read()
        self.AUDIO = QuranAudio()
        self.CHAPTER_SIZES = self.get_surah_sizes()
    
    @staticmethod
    def get_english_parallel(verse_json:dict) -> Iterable[str]:
        return verse_json["ENGLISH"].values()

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
        
    @staticmethod
    def get_crossreference_kabbalah(verse_json:dict,top_n:int=3) -> List[str]:
        return verse_json["CROSS_REFERENCE"]["KABBALAH"][:max(min(top_n,10),0)]
    
    def get_surah_sizes(self) -> List[int]:
        prev_chapter = "1"
        prev_verse = None
        surah_sizes = []
        for verse_key in self.VERSE_NAMES:
            chapter,verse = verse_key.split(":")
            if chapter != prev_chapter:
                surah_sizes.append(int(prev_verse))
                prev_chapter = chapter
            prev_verse = verse
        surah_sizes.append(int(prev_verse))
        return surah_sizes

    def get_chapter_name(self,chapter_index:str) -> str:
        return self.CHAPTER_NAMES[int(chapter_index)-1]

    def get_verse_json(self,chapter:str,verse:str) -> dict:
        with urlopen(self.URL.format(scripture = self.NAME, book_chapter_verse=f"{chapter}/{verse}")) as url:
            return loads(url.read().decode())
        #with open(f"data/{self.NAME}/{chapter}/{verse}.json") as json_file:
        #    return load(json_file)

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


class TanakhAudio:
    def __init__(self) -> None:
        self.URL = "https://raw.githubusercontent.com/mohammedterryjack/quran-data/master/audio-tanakh/{filename}.mp3?raw=true"

    def url(self, cannon:str, book:str, chapter:int) -> str:
        """ get url of audio file for book """
        return self.URL.format(filename=f"{cannon}_{book.replace('%20','%2520')}_{chapter}")

class Tanakh(HolyScripture):
    def __init__(self) -> None:
        super().__init__(scripture_name="tanakh") 
        self.BOOKS = self._METADATA["BOOKS"]
        self.AUDIO = TanakhAudio()

    def get_verse_json(self,collection:str,book:str,chapter:str,verse:str) -> dict:
        #with urlopen(self.URL.format(scripture = self.NAME, book_chapter_verse=f"{collection}/{book.replace(' ','%2520')}/{chapter}/{verse}")) as url:
        #    return loads(url.read().decode())
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

class Kabbalah(HolyScripture):
    def __init__(self) -> None:
        super().__init__(scripture_name="kabbalah")
        self.BOOKS = self._METADATA["BOOKS"]
        self.AUDIO = None
    
    def get_verse_json(self,book:str,chapter:str,verse:str) -> dict:
        #with urlopen(self.URL.format(scripture = self.NAME, book_chapter_verse=f"{book.replace(' ','%2520')}/{chapter}/{verse}")) as url:
        #    return loads(url.read().decode())
        with open(f"data/{self.NAME}/{book.replace(' ','%20')}/{chapter}/{verse}.json") as json_file:
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