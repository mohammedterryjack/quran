############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set,Optional,Tuple
from json import load
############ INSTALLED IMPORTS ###########################
from pandas import read_json
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import cosine_similarity_for_sets
##########################################################
class AudioFiles:
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
        )[min(max(reciter,0),2)]
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


def semantic_features_for_verse(verse:str, verse_names:List[str], quran_features:dict) -> Set[str]:
    index = str(VERSE_NAMES.index(verse))
    return set(quran_features[index])

def semantic_features(quran_features:dict) -> Iterable[Set[str]]:
    for index in quran_features:
        yield set(quran_features[index])
    
def list_english_translations_for_all_verses(quran_en:dict) -> Iterable[Tuple[str,str]]:
    for verse in quran_en:
        for translator in range(0,17):
            yield verse,quran_en[verse]["ENGLISH"][translator]

def arabic_verse(verse:str,quran_ar:dict) -> str:
    return quran_ar[verse]["ARABIC"]

def english_translation_of_verse(verse:str,quran_en:dict,translator:Optional[int]=8) -> str:
    parallel_translations_of_verse = quran_en[verse]["ENGLISH"]
    return parallel_translations_of_verse[max(min(translator,17),0)] if translator else parallel_translations_of_verse

def similar_verses_to_verse(verse:str, quran:dict, top_n:int=3) -> List[str]:
    return quran[verse][:max(min(top_n,10),0)]

def semantically_similar_verses_to_query(query_features:Set[str],quran_features:dict,verse_names:List[str],top_n:int=3) -> List[str]:
    semantic_scores = list(
        map(
            lambda verse_features: cosine_similarity_for_sets(
                features_a=query_features,
                features_b=verse_features
            ),
            semantic_features(quran_features)
        )
    )
    verse_indexes = argsort(semantic_scores)[:-top_n-1:-1]
    return list(map(lambda index:verse_names[index], verse_indexes))


QURAN_AUDIO = AudioFiles()
QURAN = read_json("data/mushaf/quran.json")
QURAN_EN = read_json("data/mushaf/quran_en.json")
QURAN_AR = read_json("data/mushaf/quran_ar.json")
with open("data/mushaf/quran_features.json") as json_file:
    QURAN_FEATURES = load(json_file)
VERSE_NAMES = list(QURAN_EN.keys())
with open("html_templates/main_page.html") as html_file:
    MAIN_PAGE_TEMPLATE = html_file.read()
