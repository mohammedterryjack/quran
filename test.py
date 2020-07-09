############   NATIVE IMPORTS  ###########################
from typing import List
############ INSTALLED IMPORTS ###########################
from pandas import read_json
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
from data_analysis.utils import similarity_of_two_sets_of_features
##########################################################

quran = read_json("data/quran.json")
quran_en = read_json("data/quran_en.json")

def english_translation_of_verse(verse:str,quran_en:dict,translator:int=5) -> str:
    return quran_en[verse]["ENGLISH"][max(min(translator,17),0)]

def similar_verses_to_verse(verse:str, quran:dict, top_n:int=3) -> List[str]:
    return quran[verse]["CROSS-REFERENCE"][:max(min(top_n,10),0)]

def similar_verses_to_query(query:str,quran:dict,quran_en:dict,top_n:int=3) -> List[str]:
    query_semantic_features = set_of_semantic_features_for_sentence(query)
    semantic_similarity_scores = quran["SEMANTIC FEATURES"].apply(
        lambda verse_semantic_features: similarity_of_two_sets_of_features(
            features_a=verse_semantic_features,
            features_b=query_semantic_features
        )
    )
    most_similar_indexes = argsort(semantic_similarity_scores.to_list())[:-top_n-1:-1]
    print(most_similar_indexes)

verse = "114:6"
print(english_translation_of_verse(verse=verse,quran_en=quran_en))
print(similar_verses_to_verse(verse=verse,quran=quran))
