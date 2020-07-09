############   NATIVE IMPORTS  ###########################
############ INSTALLED IMPORTS ###########################
from pandas import read_csv
############   LOCAL IMPORTS   ###########################
##########################################################

quran = read_csv("data/quran_cross_referenced.csv", sep="\t")

while True:
    translator = max(0,min(17,int(input("\nEnter a number between 0 and 17: "))))
    example_verse = input("\n>")

    example_cross_references = quran[quran["VERSE"]==example_verse]["CROSS-REFERENCE"]
    example_cross_references = example_cross_references.to_list()[0].strip("[]").split(",")
    for cross_reference in example_cross_references:
        verse_name = cross_reference.lstrip(" '").rstrip("'")
        translations = quran["ENGLISH"][quran["VERSE"]==verse_name].to_list()[0].split("\n")
        example_translation = translations[translator].lstrip(f"{translator}").strip()
        print(f"{verse_name} = {example_translation}")

