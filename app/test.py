############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from pandas import read_csv
############   LOCAL IMPORTS   ###########################
##########################################################

quran_cross_references = read_csv("../data/quran_cross_referenced.csv", sep="\t")
quran_translation = read_csv("../data/quran_english.csv", sep="\t")

example_verse = input("\n>")

example_cross_references = quran_cross_references[quran_cross_references["VERSE"]==example_verse]["CROSS-REFERENCE"]
example_cross_references = example_cross_references.to_list()[0].strip("[]").split(",")
for cross_reference in example_cross_references:
    verse_name = cross_reference.lstrip(" '").rstrip("'")
    example_translation = quran_translation[quran_translation["VERSE"]==verse_name]["0"]
    print(verse_name, example_translation.to_list()[0])
