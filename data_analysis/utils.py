############   NATIVE IMPORTS  ###########################
from typing import Dict, Set
############ INSTALLED IMPORTS ###########################
from pandas import read_csv, concat, DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from numpy import argsort
############   LOCAL IMPORTS   ###########################
##########################################################
class RawQuranArabicGrammarCSVHeaders:
    _PATH = "../raw_data/{filename}"
    _FILENAME = "quran_arabic_grammar.txt"
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

def save_searchable_quran_to_file(filename:str, arabic_feature_sets:Dict[str,Set[str]]) -> None:
    """ this stores the quran in a format that can be queried for similar verses to csv file (verse similarities are pre-computed) """
    data = DataFrame(
        arabic_feature_sets.items(),
        columns = ["VERSE","FEATURE"]
    )
    data["CROSS-REFERENCE"] = data["FEATURE"].apply(
        lambda feature_set_a: argsort(
            map(
                lambda feature_set_b: similarity_of_two_sets_of_features(
                    features_a=feature_set_b,
                    features_b=feature_set_a
                ),
                arabic_feature_sets.values()
            )
        )[:10]
    )
    data = data.set_index('VERSE')
    data.to_csv(filename, columns=["CROSS-REFERENCE"], sep="\t")


save_searchable_quran_to_file(
    arabic_feature_sets = generate_arabic_feature_set(
        arabic_features=analyse_quran_arabic_grammar_file()
    ),
    filename="../data/quran.csv"
)