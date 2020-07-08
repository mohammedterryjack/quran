############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
from utils import (
    analyse_quran_english_parallels_file
)
##########################################################

analyse_quran_english_parallels_file().to_csv(
    "../data/quran_english.csv", 
    sep="\t"
)
