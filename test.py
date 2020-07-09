############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set
############ INSTALLED IMPORTS ###########################
from pandas import read_json
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import (
    set_of_semantic_features_for_sentence,
    similarity_of_two_sets_of_features
)
##########################################################

quran = read_json("data/quran.json")
quran_en = read_json("data/quran_en.json")

def semantic_features(quran:dict) -> Iterable[Set[str]]:
    for verse in quran:
        yield set(quran[verse]["SEMANTIC FEATURES"])

def english_translation_of_verse(verse:str,quran_en:dict,translator:int=6) -> str:
    return quran_en[verse]["ENGLISH"][max(min(translator,17),0)]

def similar_verses_to_verse(verse:str, quran:dict, top_n:int=3) -> List[str]:
    return quran[verse]["CROSS-REFERENCE"][:max(min(top_n,10),0)]

def similar_verses_to_query(query:str,quran:dict,top_n:int=3) -> List[str]:
    verse_names = list(quran.keys())
    query_features = set_of_semantic_features_for_sentence(query)
    semantic_scores = list(
        map(
            lambda verse_features: similarity_of_two_sets_of_features(
                features_a=query_features,
                features_b=verse_features
            ),
            semantic_features(quran)
        )
    )
    print(max(semantic_scores))
    return list(
        map(
            lambda verse_index:verse_names[verse_index],
            argsort(semantic_scores)[:-top_n-1:-1] 
        )
    )

while True:
    query = input(">")
    similar_verses = similar_verses_to_query(query=query,quran=quran, top_n=2)
    for verse in similar_verses:
        related_verses = similar_verses_to_verse(verse=verse,quran=quran)
        for verse in related_verses:
            print(verse)
            print(english_translation_of_verse(verse=verse,quran_en=quran_en))
            print()
