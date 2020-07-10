############   NATIVE IMPORTS  ###########################f
from typing import Set, Tuple, List
from itertools import chain
############ INSTALLED IMPORTS ###########################
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize
############   LOCAL IMPORTS   ###########################
##########################################################
parent_synsets_for_synset = lambda synset:[synset] + list(synset.closure(lambda parent_synset:parent_synset.hypernyms()))
parent_synsets_for_synsets = lambda synsets: list(chain.from_iterable(map(parent_synsets_for_synset, synsets)))

def part_of_speech(tokens:List[str]) -> List[Tuple[str,str]]:
    """ 
    tags tokens using nltk and then converts tag format to wordnet's format
    ignoring irrelevant tags like DET
    """
    WORDNET_POS_MAP = {
        "VERB":wordnet.VERB,
        "ADJ":wordnet.ADJ,
        "ADV":wordnet.ADV,
        "NOUN":wordnet.NOUN
    }
    return list(
        filter(
            lambda token_pos: token_pos[1] is not None,
            map(
                lambda token_pos: (
                    token_pos[0],
                    WORDNET_POS_MAP.get(token_pos[1])
                ),
                pos_tag(tokens,tagset="universal")
            )
        )
    )


def set_of_semantic_features_for_word(word:str, part_of_speech:str) -> Set[str]:
    """ 
    uses wordnet to return a semantic concepts related to a given word
    """
    root_synsets = wordnet.synsets(word,pos=part_of_speech)
    if not any(root_synsets):
        root_synsets = wordnet.synsets(word)
    return set(
        map(
            lambda synset:synset.name(), 
            parent_synsets_for_synsets(root_synsets)
        )
    )


def set_of_semantic_features_for_sentence(sentence:str) -> Set[str]:
    """
    returns a set of semantic features for a given sentence 
    """
    return set(
        chain.from_iterable(
            map(
                lambda token_pos:set_of_semantic_features_for_word(*token_pos),
                part_of_speech(word_tokenize(sentence))
            )
        )
    )

def set_of_semantic_features_for_sentences(sentences:List[str]) -> Set[str]:
    """
    returns a single set of semantic features for a synonymous group of sentences 
    """
    return set(chain.from_iterable(map(set_of_semantic_features_for_sentence,sentences)))


def similarity_of_two_sets_of_features(features_a:set, features_b:set) -> float:
    """ 
    returns a similarity score given two sets. 
    1.0=Identical. 0.0=Nothing in Common
    """
    features_in_common = features_a.intersection(features_b)
    features_in_total = features_a | features_b
    return  len(features_in_common) / len(features_in_total)
