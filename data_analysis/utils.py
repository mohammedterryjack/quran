############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from pandas import read_csv
from sklearn.feature_extraction.text import CountVectorizer
############   LOCAL IMPORTS   ###########################
##########################################################
class QuranArabicGrammarCSVHeaders:
    _PATH = "../data/{filename}"
    _FILENAME = "quran_arabic_grammar.txt"
    _DELIMITER = "\t"
    WORD_INDEX = "LOCATION"
    WORD = "FORM"
    POS_TAG = "TAG"
    FEATURES = "FEATURES"
    _FEATURE_DELIMITER = "|"
    _LEMMA_PREFIX = "LEM:"
    _ROOT_PREFIX = "ROOT:"

def analyse_quran_arabic_grammar_file() -> None:
    quran = read_csv(
        filepath_or_buffer=QuranArabicGrammarCSVHeaders._PATH.format(
            filename=QuranArabicGrammarCSVHeaders._FILENAME
        ), 
        sep=QuranArabicGrammarCSVHeaders._DELIMITER, 
        header=0
    )
    features = quran[QuranArabicGrammarCSVHeaders.FEATURES].apply(
        lambda features_as_string:features_as_string.split(QuranArabicGrammarCSVHeaders._FEATURE_DELIMITER)
    )
    words = features.apply(
       lambda features_as_list:features_as_list[2].lstrip(
           QuranArabicGrammarCSVHeaders._LEMMA_PREFIX
        ) if len(features_as_list)>2 and features_as_list[2].startswith(
            QuranArabicGrammarCSVHeaders._LEMMA_PREFIX
        ) else features_as_list[1]
    )
    roots = features.apply(
       lambda features_as_list:features_as_list[3].lstrip(
           QuranArabicGrammarCSVHeaders._ROOT_PREFIX
       ) if len(features_as_list)>3 and features_as_list[3].startswith(
           QuranArabicGrammarCSVHeaders._ROOT_PREFIX
       ) else None
    )
    root_ngrams = roots.apply(
        lambda root: CountVectorizer(
            ngram_range=(1,3),
            analyzer="char",
            lowercase=False
        ).fit([root]).get_feature_names() if root else []
    )
    print(root_ngrams)

    indexes = quran[QuranArabicGrammarCSVHeaders.WORD_INDEX].apply(
        lambda index_as_string:list(map(int,index_as_string.strip("()").split(":")))
    )
    chapters = indexes.apply(
        lambda index:index[0]
    )
    verses = indexes.apply(
        lambda index:index[1]
    )

    #print(chapters)
    #print(verses)
    #print(words)
    #print("vocab size = ",len(set(words)))

analyse_quran_arabic_grammar_file()