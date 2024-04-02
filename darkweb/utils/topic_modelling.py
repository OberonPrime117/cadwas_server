import pandas as pd
import gensim
import json
from gensim.models import LdaModel
from gensim.corpora import Dictionary
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import json

def preprocess_text(text):
    if pd.notnull(text):
        text = text.lower()
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token.isalpha()]
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return tokens
    else:
        return []


def words(lst,corpus,dictionary,processed_comments):
    num_topics = 2
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    topics_words = []
    for topic_id, topic_words in lda_model.print_topics():
        words = [word.split('*')[1].strip().replace('"', '') for word in topic_words.split('+')]
        topics_words.append(words)
    domains = {
        'drugs': ['drugs','drug','mephedrone','narcotics', 'substance','dioxide','medicines','chemicals','mixture','Meth','DMD','synthetic substance','Methyl​enedioxy​methamphetamine','MDMA','LSD','Lysergic acid diethylamide','Ganja','diacetylmorphine','diamorphine','Opioid'],
        'pornography': ['pornography', 'adult', 'explicit'],
        'fraud': ['fraud', 'scam', 'deceit'],
        'neutral': ['neutral'],
        'bitcoin': ['bitcoin', 'cryptocurrency', 'crypto']
    }
    word_embeddings = gensim.models.Word2Vec(processed_comments, vector_size=100, window=5, min_count=1, workers=4)
    for i, topic_words in enumerate(topics_words):
        domain_scores = {domain: 0 for domain in domains.keys()}
        for word in topic_words:
            if word not in word_embeddings.wv:
                continue
            for domain, keywords in domains.items():
                if all(keyword in word_embeddings.wv for keyword in keywords):
                    similarity_score = word_embeddings.wv.n_similarity([word], keywords)
                    domain_scores[domain] += similarity_score
        most_relevant_domain = max(domain_scores, key=domain_scores.get)
        AA = [most_relevant_domain]
        for keyword in domains[most_relevant_domain]:
            ls =[]
            if keyword in word_embeddings.wv:
                similar_words = word_embeddings.wv.most_similar(keyword, topn=25)
                for word, score in similar_words:
                    ls.append(word)
                    # print(f"{word}: {score}")
            AA.append(ls)
    return AA
