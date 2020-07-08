############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from pandas import read_csv
############   LOCAL IMPORTS   ###########################
##########################################################

quran_cross_references = read_csv("data/quran_cross_references.csv")
quran_translation = read_csv("data/quran_english.csv")

example_verse = "1:1"

example_cross_references = quran_cross_references[example_verse]["CROSS-REFERENCE"]
for cross_reference in example_cross_references:
    first_translation = quran_translation[cross_reference][0]
    print(first_translation)