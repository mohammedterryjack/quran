############   NATIVE IMPORTS  ###########################
from typing import List,Iterable,Set,Optional
from difflib import get_close_matches
############ INSTALLED IMPORTS ###########################
from pandas import read_json
############   LOCAL IMPORTS   ###########################
from data_analysis.semantic_featuriser import (
    set_of_semantic_features_for_sentence,
    similarity_of_two_sets_of_features,
    cosine_similarity_for_sets
)
##########################################################

quran = read_json("data/quran.json")
quran_features = read_json("data/quran_features.json")
quran_en = read_json("data/quran_en.json")

def semantic_features(quran_features:dict) -> Iterable[Set[str]]:
    for verse in quran_features:
        yield set(quran_features[verse]["SEMANTIC FEATURES"])

def list_english_translations_for_all_verses(quran_en:dict) -> Iterable[Tuple[str,str]]:
    for verse in quran_en:
        for translator in range(0,17):
            yield verse,quran_en[verse]["ENGLISH"][translator]

def english_translation_of_verse(verse:str,quran_en:dict,translator:Optional[int]=8) -> str:
    parallel_translations_of_verse = quran_en[verse]["ENGLISH"]
    return parallel_translations_of_verse[max(min(translator,17),0)] if translator else parallel_translations_of_verse

def similar_verses_to_verse(verse:str, quran:dict, top_n:int=3) -> List[str]:
    return quran[verse]["CROSS-REFERENCE"][:max(min(top_n,10),0)]

def most_semantically_similar_verse_to_query(query:str,quran_features:dict) -> str:
    verse_names = list(quran_features.keys())
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

def most_syntactically_similar_verse_to_query(query:str,quran_en:dict) -> str:
    verses,translations = list(list_english_translations_for_all_verses(quran_en))
    print(verses)

    #similar_verse = get_close_matches(word=query,possibilities=)

while True:
    query = input(">")
    most_syntactically_similar_verse_to_query(query=query,quran=quran_en)
    verse = most_semantically_similar_verse_to_query(query=query,quran_features=quran_features)
    related_verses = similar_verses_to_verse(verse=verse,quran=quran)
    for verse in related_verses:
        print(verse)
        print(english_translation_of_verse(verse=verse,quran_en=quran_en))
        print()
