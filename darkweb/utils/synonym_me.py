import nltk
from nltk.corpus import wordnet

def get_synonyms(word):
    synsets = wordnet.synsets(word)
    synonyms = []
    for synset in synsets:
        for lemma in synset.lemmas():
            synonyms.append(lemma.name())
    return synonyms