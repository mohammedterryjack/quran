# Qur'an
Cross-reference verses of the  Quran (in Arabic and English) with Jewish source texts (in Hebrew and English)

![](design/interface.png)

https://bref-saucisson-56522.herokuapp.com/quran/1/1

## TODO

### Data
- ✅ Get Quran arabic from arabic corpus
- ✅ Get word-by-word translation from arabic corpus
- ✅ scrape together parallel english translations 
- ✅ Get arabic verses of Quran to display
- ✅ get audio of quran in hafs (mishary), warsh (jazari), hamza (sufi)
- ✅ Get tanakh for cross-referencing 
- get ahmad zaki translation of quran
- ✅ get aisha bewley translation of quran
- ✅ get kabballah>sefer yetzira & zohar in hebrew and english from sefaria
- include parallel translation of septuagint (with additional books)

### Backend AI / NLP (python3)
- ✅ store each verse of quran in arabic and parallel english (csv)
- ✅ encode each verse by arabic root letters + arabic bigram root letters + arabic trigram root letters + arabic words + morph features and cross-reference against each other and save cross-reference results for later retrieval
- ✅ encode query into wordnet vectors
- ✅ improve cross-reference results using wordnet vectors 
- ✅ improve cross-reference results using morphological vectors
- ✅ encode each verse by wordnet vectors + save vectors
- ✅ encode sefaria data into same space
- ✅ encode kabbalah data in same space
- ✅ Automatically segment Hebrew Audio so its in verses?
- ✅ Automatically segment Arabic Hamza Recitation so its in verses
- ✅ inverse feature vectors so can search verses by feature (eg name of prophet) - this would also speed up semantic search
- fix errors with bewley translation
- complete segmentation of audio files

### Backend Functions (python3)
- ✅ index search quran by chapter
- ✅ index search quran by verse
- ✅ fuzzy search words/strings across quran verses
- ✅ semantic search words/strings across quran verses
- ✅ search verse of quran against quran 
- ✅ display what features the match was based on 
- ✅ display arabic verse
- ✅ search verse of quran against sefaria
- parallel translation for english texts of tanakh/septuagint

### Deployment (python3 - flask, heroku)
- ✅ setup a basic flask
- ✅ search by verse, 
- ✅ search by chapter, 
- ✅ display arabic 
- ✅ display english parallel
- ✅ play audio (arabic)
- ✅ play audio (bible)
- ✅ search by string, 
- ✅ host backend on heroku
- ✅ reduce memory somehow
- ✅dropdown for chapter (quran and bible)
- ✅dropdown for verse (quran and bible)
- ✅Audhubillah all three autoplay when going to verse which doesn't exist
- add names of translators
- allow users to create/compile source sheets (with audio) - e.g. a wird

### Frontend (css/html/js)
- ✅ implement minimalist design 
- sliding bar to show how far you are in the book
- implement mock design frontend