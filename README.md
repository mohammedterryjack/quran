# Qur'an
Cross-reference verses of the  Quran (in Arabic and English) with Jewish source texts (in Hebrew and English)

![](design/interface.png)


## TODO

### Data
- ✅ Get Quran arabic from arabic corpus
- ✅ Get word-by-word translation from arabic corpus
- ✅ scrape together parallel english translations 
- get audio of quran in hafs (mishary), warsh (jazari), hamza (sufi)
- Access sefaria api for cross-referencing material

### Backend AI / NLP (python3)
- ✅ store each verse of quran in arabic and parallel english (csv)
- ✅ encode each verse by arabic root letters + arabic bigram root letters + arabic trigram root letters + arabic words + morph features and cross-reference against each other and save cross-reference results for later retrieval
- ✅ encode query into wordnet vectors
- ✅ improve cross-reference results using wordnet vectors 
- ✅ encode each verse by wordnet vectors + save vectors
- encode sefaria data into same space
- compare encoded query to all verses in quran fast using dot product/matrix factorisation

### Backend Functions (python3)
- index search quran by chapter
- index search quran by verse
- fuzzy search words/strings across quran verses
- semantic search words/strings across quran verses
- ✅ search verse of quran against quran 
- search verse of quran against sefaria

### Deployment (python3 - flask, heroku)
- setup a basic flask
- minimalist interface (search by verse, search by chapter, search by string, display arabic alongside english parallel, play audio)
- host backend on heroku

### Frontend (css/html/js)
- implement mock design frontend