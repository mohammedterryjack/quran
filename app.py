############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from flask import Flask
############   LOCAL IMPORTS   ###########################
from utils import (
    QURAN_AUDIO, QURAN, QURAN_EN, QURAN_AR, QURAN_FEATURES,
    VERSE_NAMES,semantic_features_for_verse,arabic_verse, 
    english_translation_of_verse, similar_verses_to_verse,
    semantically_similar_verses_to_query,QURAN_VERSE_TEMPLATE,
    BIBLE_VERSE_TEMPLATE,BIBLE_AUDIO,BIBLE_EN,BIBLE_HE,get_biblical_verse,
    format_sentence_for_html
)
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
##########################################################
app = Flask(__name__)

@app.route('/bible/<cannon>/<book>/<chapter>/<verse>')
def display_bible_verse(cannon:str,book:str,chapter:str,verse:str) -> str:
    return BIBLE_VERSE_TEMPLATE.format(
        cannon=cannon.title(),
        book=book.title(),
        chapter=chapter,
        verse=verse,
        verse_in_english=format_sentence_for_html(
            sentence=get_biblical_verse(
                bible_translation=BIBLE_EN,
                cannon=cannon,
                book=book,
                chapter=int(chapter),
                verse=int(verse)
            )
        ),
        verse_in_hebrew=get_biblical_verse(
            bible_translation=BIBLE_HE,
            cannon=cannon,
            book=book,
            chapter=int(chapter),
            verse=int(verse)
        ),
        audio_hebrew=BIBLE_AUDIO.url(
            cannon=cannon,
            book=book,
            chapter=chapter
        )
    )

@app.route('/quran/<chapter>/<verse>')
def display_quranic_verse(chapter:str,verse:str) -> str:
    verse_key = f"{chapter}:{verse}"
    return QURAN_VERSE_TEMPLATE.format(
        chapter=chapter,
        verse=verse,
        verse_audio_hafs=QURAN_AUDIO.url(
            verse_name=verse_key,
            reciter=0
        ),
        verse_audio_warsh=QURAN_AUDIO.url(
            verse_name=verse_key,
            reciter=1
        ),
        verse_in_arabic=arabic_verse(
            verse=verse_key,
            quran_ar=QURAN_AR
        ),
        verse_in_english=format_sentence_for_html(
            sentence=english_translation_of_verse(
                verse=verse_key,
                quran_en=QURAN_EN
            )
        ),
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
#         common_features = query_features.intersection(verse_features)
#         print(common_features)
#         for related_verse in similar_verses_to_verse(verse=verse,quran=QURAN):
#             print("\t",related_verse)
#             print("\t",english_translation_of_verse(verse=related_verse,quran_en=QURAN_EN))
#             print("\t",arabic_verse(verse=verse,quran_ar=QURAN_AR))
