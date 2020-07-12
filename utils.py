############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set,Optional,Tuple
from json import load
############ INSTALLED IMPORTS ###########################
from pandas import read_json
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import cosine_similarity_for_sets
##########################################################
class QuranAudioFiles:
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

class BibleAudioFiles:
    def __init__(self) -> None:
        self.URL = "http://www.mechon-mamre.org/mp3"
        self.AUDIO_FORMAT = "mp3"
        self.BOOKS = {
            "torah/genesis":"01","torah/exodus":"02","torah/leviticus":"03","torah/numbers":"04","torah/deuteronomy":"05",
            "prophets/joshua":"06","prophets/judges":"07","prophets/i%20samuel":"08a","prophets/ii%20samuel":"08b",
            "prophets/i%20kings":"09a","prophets/ii%20kings":"09b","prophets/isaiah":"10","prophets/jeremiah":"11",
            "prophets/ezekiel":"12","prophets/hosea":"13","prophets/joel":"14","prophets/amos":"15","prophets/obadiah":"16",
            "prophets/jonah":"17","prophets/micah":"18","prophets/nahum":"19","prophets/habakkuk":"20",
            "prophets/zephaniah":"21","prophets/haggai":"22","prophets/zechariah":"23","prophets/malachi":"24",
            "writings/i%20chronicles":"25a","writings/ii%20chronicles":"25b","writings/psalms":"26","writings/job":"27",
            "writings/proverbs":"28","writings/ruth":"29","writings/song%20of%20songs":"30","writings/ecclesiastes":"31",
            "writings/lamentations":"32","writings/esther":"33","writings/daniel":"34","writings/ezra":"35a","writings/nehemia":"35b"
        }

    def url(self, cannon:str, book:str, chapter:int) -> str:
        """ get url of audio file for book """
        return f"{self.URL}/t{self.BOOKS.get(f'{cannon.title()}/{book.title()}')}{str(chapter).zfill(2)}.{self.AUDIO_FORMAT}"

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


def get_bible(language_code:str) -> dict:
    bible = {}
    for book_name in BIBLE_AUDIO.BOOKS:
        directory,book = book_name.lower().split("/")
        if directory not in bible:
            bible[directory] = {}
        path = f"data/tanakh/{directory}/{book}_{language_code}.json"
        try:
            with open(path,encoding='utf-8') as json_file:
                BOOK = load(json_file)["text"]
            bible[directory][book] = BOOK
        except:
            print(directory,book)
    return bible 


def get_biblical_verse(bible_translation:dict, cannon:str, book:str, chapter:int, verse:int) -> str:
    return bible_translation[cannon][book][chapter-1][verse-1]

def format_sentence_for_html(sentence:str) -> str:
    return sentence.replace(",",",<br>").replace(";",";<br>").replace(
        ":",":<br>").replace(".",".<br><br>").replace(
        "!","!<br><br>").replace("?","?<br><br>")

QURAN_AUDIO = QuranAudioFiles()
BIBLE_AUDIO = BibleAudioFiles()
QURAN = read_json("data/mushaf/quran.json")
QURAN_EN = read_json("data/mushaf/quran_en.json")
QURAN_AR = read_json("data/mushaf/quran_ar.json")
with open("data/mushaf/quran_features.json") as json_file:
    QURAN_FEATURES = load(json_file)
VERSE_NAMES = list(QURAN_EN.keys())
with open("html_templates/quran_verse.html") as html_file:
    QURAN_VERSE_TEMPLATE = html_file.read()
with open("html_templates/bible_verse.html") as html_file:
    BIBLE_VERSE_TEMPLATE = html_file.read()
BIBLE_EN = get_bible(language_code="en")
BIBLE_HE = get_bible(language_code="he")