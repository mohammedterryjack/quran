# Qur'an
Cross-reference verses of the  Quran (in Arabic and English) with Jewish source texts (in Hebrew and English)

![](design/interface.png)


## TODO

### Data
- Get Quran arabic from arabic corpus
- Get word-by-word translation from arabic corpus
- scrape together parallel english translations 
- get audio of quran in hafs (mishary), warsh (jazari), hamza (sufi)
- Access sefaria api for cross-referencing material

### Backend (python3)
- display/store each verse of quran in arabic and parallel english (csv)
- display/store each arabic word of quran with grammar and parallel english (csv)
- index search quran by chapter
- index search quran by verse
- fuzzy search words/strings across quran and sefaria
- semantic search words/strings across quran and sefaria
- fuzzy search select verse of quran against quran and sefaria
- semantic search select verse of quran against quran and sefaria

### Deployment
- basic flask
- minamilist interface (search by verse, search by chapter, search by string, display arabic alongside english parallel, play audio)
- host backend on heroku

### Polishing
- implement mock design frontend in css/html/js