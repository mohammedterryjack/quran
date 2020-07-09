############   NATIVE IMPORTS  ###########################
from typing import Dict, Set
############ INSTALLED IMPORTS ###########################
from pandas import read_csv, concat, DataFrame, set_option
from sklearn.feature_extraction.text import CountVectorizer
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from semantic_featuriser import set_of_semantic_features_for_sentences
##########################################################
class RawQuranEnglishParallels:
    _PATH = "../raw_data/{filename}.txt"
    _FILENAME = "quran_english_translations"
    _CHAPTER_VERSE_SEPARATOR = "-"

class RawQuranArabicGrammarCSVHeaders:
    _PATH = "../raw_data/{filename}.txt"
    _FILENAME = "quran_arabic_grammar"
    _DELIMITER = "\t"
    WORD_INDEX = "LOCATION"
    WORD = "FORM"
    POS_TAG = "TAG"
    FEATURES = "FEATURES"
    _FEATURE_DELIMITER = "|"
    _LEMMA_PREFIX = "LEM:"
    _ROOT_PREFIX = "ROOT:"

def analyse_quran_arabic_grammar_file() -> DataFrame:
    """ 
    given the raw datafile obtained from http://corpus.quran.com/
    containing the quran and its morphological and syntactic features for each word in the quran 
    The most important features are extracted for later analysis
    """
    quran = read_csv(
        filepath_or_buffer=RawQuranArabicGrammarCSVHeaders._PATH.format(
            filename=RawQuranArabicGrammarCSVHeaders._FILENAME
        ), 
        sep=RawQuranArabicGrammarCSVHeaders._DELIMITER, 
        header=0
    )
    pos_tags = quran[RawQuranArabicGrammarCSVHeaders.POS_TAG].apply(
        lambda pos_tag:f"POS:{pos_tag}"
    )
    features = quran[RawQuranArabicGrammarCSVHeaders.FEATURES].apply(
        lambda features_as_string:features_as_string.split(RawQuranArabicGrammarCSVHeaders._FEATURE_DELIMITER)
    )
    words = features.apply(
       lambda features_as_list:features_as_list[2].lstrip(
           RawQuranArabicGrammarCSVHeaders._LEMMA_PREFIX
        ) if len(features_as_list)>2 and features_as_list[2].startswith(
            RawQuranArabicGrammarCSVHeaders._LEMMA_PREFIX
        ) else features_as_list[1]
    )
    roots = features.apply(
       lambda features_as_list:features_as_list[3].lstrip(
           RawQuranArabicGrammarCSVHeaders._ROOT_PREFIX
       ) if len(features_as_list)>3 and features_as_list[3].startswith(
           RawQuranArabicGrammarCSVHeaders._ROOT_PREFIX
       ) else None
    )
    root_ngrams = roots.apply(
        lambda root: CountVectorizer(
            ngram_range=(1,3),
            analyzer="char",
            lowercase=False
        ).fit([root]).get_feature_names() if root else []
    )
    indexes = quran[RawQuranArabicGrammarCSVHeaders.WORD_INDEX].apply(
        lambda index_as_string:list(map(int,index_as_string.strip("()").split(":")))
    )
    chapters = indexes.apply(
        lambda index:index[0]
    )
    verses = indexes.apply(
        lambda index:index[1]
    )
    return concat(
        objs=[
            chapters,
            verses,
            pos_tags,
            words,
            root_ngrams
        ],
        keys=[
            "CHAPTER",
            "VERSE",
            "PART OF SPEECH",
            "WORD",
            "ROOT N-GRAMS"
        ],
        axis=1
    )

def generate_arabic_feature_set(arabic_features:DataFrame) -> dict:
    """ 
    given arabic morphological and syntactic features 
    (e.g. arabic root letters, the word's lemma, part of speech, etc)
    for each word in the quran,
    the features are grouped by verse and 
    a set of morphological and syntactic features are returned for each verse in the quran 
    """
    vector_features = {}

    for chapter,verse,pos,word,ngrams in arabic_features.itertuples(index=False):  
        vector_key = f"{chapter}:{verse}"
        if vector_key not in vector_features:
            vector_features[vector_key] = set()

        vector_features[vector_key].add(word)
        vector_features[vector_key].add(pos)
        vector_features[vector_key] |= set(ngrams)

    return vector_features

def similarity_of_two_sets_of_features(features_a:set, features_b:set) -> float:
    """ returns a similarity score given two sets. 1.0=Identical. 0.0=Nothing in Common"""
    features_in_common = features_a.intersection(features_b)
    features_in_total = features_a | features_b
    return  len(features_in_common) / len(features_in_total)

def analyse_quran_english_parallels_file() -> DataFrame:
    with open(RawQuranEnglishParallels._PATH.format(
            filename=RawQuranEnglishParallels._FILENAME,
        ),
        encoding="utf8",
    ) as english_parallels_file:
        raw_lines = english_parallels_file.readlines()
    
    verse_name = None
    verse_translation = []
    verse_names = []
    verse_translations = []
    for raw_line in raw_lines:
        line =raw_line.strip()
        try:
            chapter_verse = line.split(RawQuranEnglishParallels._CHAPTER_VERSE_SEPARATOR)
            chapter,verse = map(int,chapter_verse)
            verse_name = f"{chapter}:{verse}"
            verse_names.append(verse_name)
            verse_translations.append([])
            line = ""
        except:
            pass

        if line and verse_name:
            verse_translations[-1].append(line)
    
    data = DataFrame(
        {
            "VERSE":verse_names,
            "ENGLISH":verse_translations
        }
    )
    return data.set_index("VERSE")

def save_searchable_quran_to_file(path:str, arabic_feature_sets:Dict[str,Set[str]], top_n_search_results:int) -> None:
    """ this stores the quran in a format that can be queried for similar verses to csv file (verse similarities are pre-computed) """
    english_quran = analyse_quran_english_parallels_file()["ENGLISH"]
    english_quran.to_csv(f"{path}/quran_en.csv", sep="|")
    quran = DataFrame(
        arabic_feature_sets.items(),
        columns = ["VERSE","MORPHOLOGICAL FEATURES"]
    )
    quran["SEMANTIC FEATURES"] = english_quran.apply(
        lambda sentences: set_of_semantic_features_for_sentences(sentences)
    )
    print(quran)
    quran["FEATURES"] = [
        morphological_features | semantic_features for morphological_features,semantic_features in zip(
            quran["MORPHOLOGICAL FEATURES"], 
            quran["SEMANTIC FEATURES"]
        )
    ]
    print(quran)
    quran["CROSS-REFERENCE SCORES"] = quran["FEATURES"].apply(
        lambda feature_set_a: list(
            map(
                lambda feature_set_b: similarity_of_two_sets_of_features(
                    features_a=feature_set_b,
                    features_b=feature_set_a
                ),
                arabic_feature_sets.values()
            )
        )
    )
    quran["CROSS-REFERENCE INDICES"] = quran["CROSS-REFERENCE SCORES"].apply(
        lambda scores:argsort(scores)[:-top_n_search_results-1:-1]
    )
    verse_names = list(arabic_feature_sets.keys())
    quran["CROSS-REFERENCE"] = quran["CROSS-REFERENCE INDICES"].apply(
        lambda verse_indexes: list(map(lambda index:verse_names[index],verse_indexes))
    )
    quran = quran.set_index('VERSE')
    quran.to_csv(f"{path}/quran.csv", columns=["CROSS-REFERENCE", "SEMANTIC FEATURES"], sep="\t")