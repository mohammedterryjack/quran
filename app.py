############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from flask import Flask, request
############   LOCAL IMPORTS   ###########################
from utils import Tanakh,Quran
from html_templates.utils import (
    format_sentences_to_be_hidden_html,
    format_and_link_verses_for_html,
    format_sentence_for_html
)
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
##########################################################
QURAN = Quran()
TANAKH = Tanakh()

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return "Coming Soon..."
    
@app.route('/quran/<chapter>/<verse>')
def display_quranic_verse(chapter:str,verse:str) -> str:
    verse_key = f"{chapter}:{verse}"
    next_verse_key = QURAN.get_next_verse_name(verse_key)
    previous_verse_key = QURAN.get_previous_verse_name(verse_key)
    VERSE_DATA = QURAN.get_verse_json(chapter,verse)
    related_quran_verses = QURAN.get_crossreference_quran(VERSE_DATA, top_n=5)
    related_quran_verses_linked = format_and_link_verses_for_html(
        scripture="quran",
        verses=related_quran_verses[1:],
        verses_to_display=map(
            QURAN.get_english_summary_via_verse_name,
            related_quran_verses[1:]
        ),
    )
    related_bible_verses = QURAN.get_crossreference_bible(VERSE_DATA, top_n=5)
    related_bible_verses_linked = format_and_link_verses_for_html(
        scripture="tanakh",
        verses=related_bible_verses,
        verses_to_display = map(
            TANAKH.get_english_summary_via_verse_name,
            related_bible_verses
        ),
    )
    return QURAN.HTML.format(
        chapter=chapter,
        verse=verse,
        chapter_name=QURAN.get_chapter_name(chapter),
        verse_audio_hafs=QURAN.AUDIO.url(verse_key,0),
        verse_audio_warsh=QURAN.AUDIO.url(verse_key,1),
        verse_in_arabic=QURAN.get_arabic(VERSE_DATA),
        verses_in_english=format_sentences_to_be_hidden_html(
            sentences=QURAN.get_english_parallel(VERSE_DATA),
            default_displayed=QURAN.DEFAULT_TRANSLATOR
        ),
        related_verses_quran=related_quran_verses_linked,
        related_verses_bible=related_bible_verses_linked,
        next_page_url = f"/quran/{next_verse_key.replace(':','/')}",
        previous_page_url = f"/quran/{previous_verse_key.replace(':','/')}"
    )

@app.route('/tanakh/<collection>/<book>/<chapter>/<verse>')
def display_bible_verse(collection:str,book:str,chapter:str,verse:str) -> str:
    book_key = book.replace(" ","%20")
    verse_key = f"{collection}:{book_key}:{chapter}:{verse}"
    next_verse_key = TANAKH.get_next_verse_name(verse_key)
    previous_verse_key = TANAKH.get_previous_verse_name(verse_key)
    VERSE_DATA = TANAKH.get_verse_json(collection,book,chapter,verse)
    return TANAKH.HTML.format(
        collection=collection.title(),
        book=book.title(),
        chapter=chapter,
        verse=verse,
        verse_in_english=format_sentence_for_html(TANAKH.get_english(VERSE_DATA)),
        verse_in_hebrew=TANAKH.get_hebrew(VERSE_DATA),
        audio_hebrew=TANAKH.AUDIO.url(collection,book_key,chapter),
        next_page_url = f"/tanakh/{next_verse_key.replace(':','/')}",
        previous_page_url = f"/tanakh/{previous_verse_key.replace(':','/')}"
    )

# @app.route('/search', methods=['GET', 'POST'])
# def search() -> str:
#     query = request.args.get('query')
#     query_features = set_of_semantic_features_for_sentence(query)
#     verses = QURAN.semantically_similar_verses_to_query(query_features, top_n=5)
#     first_verse = verses[0]
#     chapter,verse = first_verse.split(":")
#     verse_key = f"{chapter}:{verse}"
#     next_verse_key = QURAN.next_verse(verse_key)
#     previous_verse_key = QURAN.previous_verse(verse_key)
#     related_verses = format_and_link_verses_for_html(
#         verses=verses[1:],
#         verses_to_display=map(
#             lambda verse_name:QURAN.english_translation_of_verse(
#                 verse=verse_name,
#                 translator=DEFAULT_TRANSLATOR
#             )[:50],
#             verses[1:]
#         ),
#         scripture="quran"
#     )
#     bible_verse_names = BIBLE.semantically_similar_verses_to_query(query_features,top_n=5)
#     bible_verses = format_and_link_verses_for_html(
#         verses=bible_verse_names,
#         verses_to_display = map(
#             lambda verse_name:BIBLE.verse(
#                 language_code="en",
#                 cannon=verse_name.split(":")[0],
#                 book=verse_name.split(":")[1],
#                 chapter=int(verse_name.split(":")[2]),
#                 verse=int(verse_name.split(":")[3])
#             )[:50],
#             bible_verse_names
#         ),
#         scripture="bible",
#     )

#     return QURAN_VERSE_TEMPLATE.format(
#         chapter=chapter,
#         verse=verse,
#         chapter_name=QURAN.CHAPTER_NAMES()[int(chapter)-1],
#         verse_audio_hafs=QURAN_AUDIO.url(verse_key,0),
#         verse_audio_warsh=QURAN_AUDIO.url(verse_key,1),
#         verse_in_arabic=QURAN.arabic_verse(verse_key),
#         verses_in_english=format_sentences_to_be_hidden_html(
#             sentences=QURAN.english_translations_of_verse(verse_key),
#             default_displayed=6
#         ),
#         related_verses_quran=related_verses,
#         related_verses_bible=bible_verses,
#         next_page_url = f"/quran/{next_verse_key.replace(':','/')}",
#         previous_page_url = f"/quran/{previous_verse_key.replace(':','/')}",
#     )

if __name__ == '__main__':
    app.run(threaded=True, port=5000)