############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from flask import Flask, request, redirect
############   LOCAL IMPORTS   ###########################
from utils import Tanakh,Quran
from html_templates.utils import (
    format_sentences_to_be_hidden_html,
    format_and_link_verses_for_html,
    format_sentence_for_html,
    list_options_html
)
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
##########################################################
QURAN = Quran()
TANAKH = Tanakh()

app = Flask(__name__)

@app.route('/')
def verse_of_the_minute() -> str:
    verse_key = QURAN.verse_name_for_now().replace(":","/")
    return redirect(f"/quran/{verse_key}")

@app.route('/quran/<chapter>/<verse>')
def display_quranic_verse(chapter:str,verse:str) -> str:
    verse_key = f"{chapter}:{verse}"
    if verse_key not in QURAN.VERSE_NAMES:
        return QURAN.HTML_ERROR.format(
        verse_key=verse_key,
        verse_in_arabic = "أعوذُ بِٱللَّهِ مِنَ ٱلشَّيۡطَٰنِ ٱلرَّجِيمِ",
        verse_audio_hafs=QURAN.AUDIO.url("audhubillah",reciter=0),
        verse_audio_warsh=QURAN.AUDIO.url("audhubillah",reciter=1),
        verse_audio_hamza=QURAN.AUDIO.url("audhubillah",reciter=2),
    )
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
    chapter_name = QURAN.get_chapter_name(chapter)
    chapter_numbers = range(1,115)
    return QURAN.HTML.format(
        chapter=chapter,
        verse=verse,
        chapter_name=chapter_name,
        chapter_names=list_options_html(
            options=QURAN.CHAPTER_NAMES,
            urls=map(
                lambda chapter_name:f"/quran/{QURAN.CHAPTER_NAMES.index(chapter_name)+1}/1",
                QURAN.CHAPTER_NAMES
            ),
            selected_option=chapter_name
        ),
        chapter_numbers=list_options_html(
            options=chapter_numbers,
            urls=map(
                lambda chapter_number:f"/quran/{chapter_number}/1",
                chapter_numbers
            ),
            selected_option=int(chapter)
        ),
        verse_numbers=list_options_html(
            options=range(1,QURAN.CHAPTER_SIZES[int(chapter)-1]+1),
            urls= map(
                lambda verse_number:f"/quran/{chapter}/{verse_number}",
                range(1,QURAN.CHAPTER_SIZES[int(chapter)-1]+1)
            ),
            selected_option=int(verse)
        ),
        verse_audio_hafs=QURAN.AUDIO.url(verse_key,0),
        verse_audio_warsh=QURAN.AUDIO.url(verse_key,1),
        verse_audio_hamza=QURAN.AUDIO.url(verse_key,2),
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

#     related_quran_verses = QURAN.get_verse_names_relevant_to_query(query_features, top_n=5)
#     verse_key = related_quran_verses[0]
#     chapter,verse = verse_key.split(":")

#     next_verse_key = QURAN.get_next_verse_name(verse_key)
#     previous_verse_key = QURAN.get_previous_verse_name(verse_key)
#     VERSE_DATA = QURAN.get_verse_json(chapter,verse)
#     related_quran_verses = QURAN.get_crossreference_quran(VERSE_DATA, top_n=5)
#     related_quran_verses_linked = format_and_link_verses_for_html(
#         scripture="quran",
#         verses=related_quran_verses[1:],
#         verses_to_display=map(
#             QURAN.get_english_summary_via_verse_name,
#             related_quran_verses[1:]
#         ),
#     )

#     related_bible_verses = TANAKH.get_verse_names_relevant_to_query(query_features,top_n=5)
#     related_bible_verses_linked = format_and_link_verses_for_html(
#         scripture="tanakh",
#         verses=related_bible_verses,
#         verses_to_display = map(
#             TANAKH.get_english_summary_via_verse_name,
#             related_bible_verses
#         ),
#     )
#     return QURAN.HTML.format(
#         chapter=chapter,
#         verse=verse,
#         chapter_name=QURAN.get_chapter_name(chapter),
#         verse_audio_hafs=QURAN.AUDIO.url(verse_key,0),
#         verse_audio_warsh=QURAN.AUDIO.url(verse_key,1),
#         verse_audio_hamza=QURAN.AUDIO.url(verse_key,2),
#         verse_in_arabic=QURAN.get_arabic(VERSE_DATA),
#         verses_in_english=format_sentences_to_be_hidden_html(
#             sentences=QURAN.get_english_parallel(VERSE_DATA),
#             default_displayed=QURAN.DEFAULT_TRANSLATOR
#         ),
#         related_verses_quran=related_quran_verses_linked,
#         related_verses_bible=related_bible_verses_linked,
#         next_page_url = f"/quran/{next_verse_key.replace(':','/')}",
#         previous_page_url = f"/quran/{previous_verse_key.replace(':','/')}"
#     )


if __name__ == '__main__':
    app.run(threaded=True, port=5000)