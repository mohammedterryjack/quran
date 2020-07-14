############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from flask import Flask, request
############   LOCAL IMPORTS   ###########################
from utils import QuranAudio,BibleAudio,BibleText,QuranText
from html_templates.utils import (
    format_sentences_to_be_hidden_html,
    format_and_link_verses_for_html,
    format_sentence_for_html
)
from data_analysis.semantic_featuriser import set_of_semantic_features_for_sentence
##########################################################
DEFAULT_TRANSLATOR = 6
QURAN_AUDIO = QuranAudio()
QURAN = QuranText()
with open("html_templates/quran_verse.html") as html_file:
    QURAN_VERSE_TEMPLATE = html_file.read()

# BIBLE_AUDIO = BibleAudio()
# BIBLE = BibleText()
# with open("html_templates/bible_verse.html") as html_file:
#     BIBLE_VERSE_TEMPLATE = html_file.read()

app = Flask(__name__)

@app.route('/')
def hello() -> str:
    return "Coming Soon..."
    
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
    
# @app.route('/quran/<chapter>/<verse>')
# def display_quranic_verse(chapter:str,verse:str) -> str:
#     verse_key = f"{chapter}:{verse}"
#     next_verse_key = QURAN.next_verse(verse_key)
#     previous_verse_key = QURAN.previous_verse(verse_key)
#     verses = QURAN.similar_verses_to_verse(verse_key, scripture=0, top_n=5)
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
#     bible_verse_names = QURAN.similar_verses_to_verse(verse_key, scripture=1, top_n=5)
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
#         scripture="bible"
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
#             default_displayed=DEFAULT_TRANSLATOR
#         ),
#         related_verses_quran=related_verses,
#         related_verses_bible=bible_verses,
#         next_page_url = f"/quran/{next_verse_key.replace(':','/')}",
#         previous_page_url = f"/quran/{previous_verse_key.replace(':','/')}"
#     )

# @app.route('/bible/<cannon>/<book>/<chapter>/<verse>')
# def display_bible_verse(cannon:str,book:str,chapter:str,verse:str) -> str:
#     book_key = book.replace(" ","%20")
#     verse_key = f"{cannon}:{book_key}:{chapter}:{verse}"
#     next_verse_key = BIBLE.next_verse(verse_key)
#     previous_verse_key = BIBLE.previous_verse(verse_key)
#     return BIBLE_VERSE_TEMPLATE.format(
#         cannon=cannon.title(),
#         book=book.title(),
#         chapter=chapter,
#         verse=verse,
#         verse_in_english=format_sentence_for_html(
#             sentence=BIBLE.verse("en",cannon,book_key,int(chapter),int(verse))
#         ),
#         verse_in_hebrew=BIBLE.verse("he",cannon,book_key,int(chapter),int(verse)),
#         audio_hebrew=BIBLE_AUDIO.url(cannon,book_key,chapter),
#         next_page_url = f"/bible/{next_verse_key.replace(':','/')}",
#         previous_page_url = f"/bible/{previous_verse_key.replace(':','/')}"
#     )

if __name__ == '__main__':
    app.run(threaded=True, port=5000)