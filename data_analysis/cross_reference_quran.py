############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
from utils import (
    save_searchable_quran_to_file,
    generate_arabic_feature_set,
    analyse_quran_arabic_grammar_file
)
##########################################################

save_searchable_quran_to_file(
    arabic_feature_sets = generate_arabic_feature_set(
        arabic_features=analyse_quran_arabic_grammar_file()
    ),
    top_n_search_results=10,
    filename="../data/quran_cross_referenced.csv"
)