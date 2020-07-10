############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set,Optional,Tuple
from difflib import SequenceMatcher
from json import load
############ INSTALLED IMPORTS ###########################
from pandas import read_json
from numpy import argsort
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import (
    set_of_semantic_features_for_sentence,
    similarity_of_two_sets_of_features,
    cosine_similarity_for_sets
)
##########################################################

quran = read_json("data/quran.json")
quran_en = read_json("data/quran_en.json")
with open("data/quran_features.json") as json_file:
    quran_features = load(json_file)

def semantic_features(quran_features:dict) -> Iterable[Set[str]]:
    for verse in quran_features:
        yield set(quran_features[verse])

def list_english_translations_for_all_verses(quran_en:dict) -> Iterable[Tuple[str,str]]:
    for verse in quran_en:
        for translator in range(0,17):
            yield verse,quran_en[verse]["ENGLISH"][translator]

def english_translation_of_verse(verse:str,quran_en:dict,translator:Optional[int]=8) -> str:
    parallel_translations_of_verse = quran_en[verse]["ENGLISH"]
    return parallel_translations_of_verse[max(min(translator,17),0)] if translator else parallel_translations_of_verse

def similar_verses_to_verse(verse:str, quran:dict, top_n:int=3) -> List[str]:
    return quran[verse][:max(min(top_n,10),0)]

def most_semantically_similar_verse_to_query(query:str,quran_features:dict,verse_names:List[str]) -> str:
    query_features = set_of_semantic_features_for_sentence(query)
    semantic_scores = list(
        map(
            lambda verse_features: cosine_similarity_for_sets(
                features_a=query_features,
                features_b=verse_features
            ),
            semantic_features(quran_features)
        )
    )
    best_score = max(semantic_scores)
    verse_index = semantic_scores.index(best_score)
    return verse_names[verse_index]

def syntactically_similar_verse_to_query(query:str,quran_en:dict) -> List[str]:
    verses,translations = zip(*list_english_translations_for_all_verses(quran_en))
    similarity_scores = list(
        map(
            lambda translation:SequenceMatcher(None, query, translation).ratio(),
            translations
        )
    )
    best_indexes = argsort(similarity_scores)[:-4:-1]
    best_verses = list(map(lambda index:verses[index], best_indexes))
    best_verses_no_duplicates = []
    for verse in best_verses:
        if verse not in best_verses_no_duplicates:
            best_verses_no_duplicates.append(verse)
    return best_verses_no_duplicates

while True:
    query = input(">")
    # print("FUZZY")
    # verses = syntactically_similar_verse_to_query(query=query,quran_en=quran_en)
    # for verse in verses:
    #     print(verse)
    #     print(english_translation_of_verse(verse=verse,quran_en=quran_en))
    #     print()
    # print("MEANING")
    verse = most_semantically_similar_verse_to_query(
        query=query,
        quran_features=quran_features,
        verse_names = list(quran_en.keys())
    )
    related_verses = similar_verses_to_verse(verse=verse,quran=quran)
    for verse in related_verses:
        print(verse)
        print(english_translation_of_verse(verse=verse,quran_en=quran_en))
        print()
