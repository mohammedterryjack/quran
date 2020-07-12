############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from flask import Flask
############   LOCAL IMPORTS   ###########################
from utils import (
    QURAN_AUDIO, QURAN, QURAN_EN, QURAN_AR, QURAN_FEATURES,
    VERSE_NAMES,semantic_features_for_verse,arabic_verse, 
    english_translation_of_verse, similar_verses_to_verse,
    semantically_similar_verses_to_query,MAIN_PAGE_HTML_TEMPLATE
)
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
##########################################################

app = Flask(__name__)

@app.route('/')
def test():
    verse = "1:1"
    return MAIN_PAGE_HTML_TEMPLATE.format(
        verse_number=verse,
        verse_in_arabic=arabic_verse(
            verse=verse,
            quran_ar=QURAN_AR
        ),
        verse_in_english=english_translation_of_verse(
            verse=verse,
            quran_en=QURAN_EN
        )
    )

if __name__ == '__main__':
    app.run()

# while True:
#     query = input(">")
#     query_features = set_of_semantic_features_for_sentence(query)
#     verses = semantically_similar_verses_to_query(
#         query_features= query_features,
#         quran_features=QURAN_FEATURES,
#         verse_names = VERSE_NAMES
#     )
#     for verse in verses:
#         print(verse)
#         print(QURAN_AUDIO.filename(verse_name=verse,reciter=0))
#         verse_features = semantic_features_for_verse(
#             verse=verse, 
#             quran_features=QURAN_FEATURES,
#             verse_names=VERSE_NAMES
#         )
#         common_features = query_features.intersection(verse_features)
#         print(common_features)
#         for related_verse in similar_verses_to_verse(verse=verse,quran=QURAN):
#             print("\t",related_verse)
#             print("\t",english_translation_of_verse(verse=related_verse,quran_en=QURAN_EN))
#             print("\t",arabic_verse(verse=verse,quran_ar=QURAN_AR))