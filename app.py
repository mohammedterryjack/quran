############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from flask import Flask
############   LOCAL IMPORTS   ###########################
from utils import QuranAudio,BibleAudio,BibleText,QuranText
##########################################################
def format_sentence_for_html(sentence:str) -> str:
    return sentence.replace(",",",<br>").replace(";",";<br>").replace(
        ":",":<br>").replace(".",".<br><br>").replace(
        "!","!<br><br>").replace("?","?<br><br>")

QURAN_AUDIO = QuranAudio()
QURAN = QuranText()
with open("html_templates/quran_verse.html") as html_file:
    QURAN_VERSE_TEMPLATE = html_file.read()

BIBLE_AUDIO = BibleAudio()
BIBLE = BibleText()
with open("html_templates/bible_verse.html") as html_file:
    BIBLE_VERSE_TEMPLATE = html_file.read()

app = Flask(__name__)


@app.route('/bible/<cannon>/<book>/<chapter>/<verse>')
def display_bible_verse(cannon:str,book:str,chapter:str,verse:str) -> str:
    return BIBLE_VERSE_TEMPLATE.format(
        cannon=cannon.title(),
        book=book.title(),
        chapter=chapter,
        verse=verse,
        verse_in_english=format_sentence_for_html(
            sentence=BIBLE.verse("en",cannon,book,int(chapter),int(verse))
        ),
        verse_in_hebrew=BIBLE.verse("he",cannon,book,int(chapter),int(verse)),
        audio_hebrew=BIBLE_AUDIO.url(cannon,book,chapter)
    )

@app.route('/quran/<chapter>/<verse>')
def display_quranic_verse(chapter:str,verse:str) -> str:
    verse_key = f"{chapter}:{verse}"
    return QURAN_VERSE_TEMPLATE.format(
        chapter=chapter,
        verse=verse,
        chapter_name=QURAN.CHAPTER_NAMES.get(chapter),
        verse_audio_hafs=QURAN_AUDIO.url(verse_key,0),
        verse_audio_warsh=QURAN_AUDIO.url(verse_key,1),
        verse_in_arabic=QURAN.arabic_verse(verse_key),
        verse_in_english=format_sentence_for_html(
            sentence=QURAN.english_translation_of_verse(verse_key)
        ),
        related_verses=QURAN.similar_verses_to_verse(verse)
    )

if __name__ == '__main__':
    app.run()

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