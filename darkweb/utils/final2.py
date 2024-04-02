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
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import json
import numpy as np

def get_comments_list(file_path, sheet_name='Sheet1', column_name='Comments'):
    df = pd.read_excel(file_path)

    # Get the 'Comments' column as a list
    comments_list = df[column_name].tolist()
    # comments_list = comments_list[]

    return comments_list

def preprocess_text(text):
    text = str(text)
    if text:
        try:
            text = text.lower()
        except:
            text = text
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token.isalpha()]
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        return tokens
    else:
        return []

def identify_highest_correlating_domain(input_words,glove_model):
    # Load the GloVe model
    # glove_model = api.load("glove-wiki-gigaword-300")

    database_keywords = ["drugs", "violence", "weapon", "finance", "porn", "wiki", "hack", "literature", "piracy", "security", "defense", "news", "journalist"]

    def calculate_max_correlation_score(input_vector):
        max_score = 0
        max_keyword = None

        for keyword in database_keywords:
            correlation_score = np.dot(input_vector, glove_model[keyword]) / (np.linalg.norm(input_vector) * np.linalg.norm(glove_model[keyword]))
            if correlation_score > max_score:
                max_score = correlation_score
                max_keyword = keyword

        return max_score, max_keyword

    def get_contributing_words(input_words, domain_keyword):
        input_vector = np.zeros(glove_model.vector_size)

        for word in input_words:
            if word in glove_model:
                input_vector += glove_model[word]

        max_score, _ = calculate_max_correlation_score(input_vector)

        contributing_words = []
        for word in input_words:
            if word in glove_model:
                modified_vector = input_vector - glove_model[word]
                _, keyword = calculate_max_correlation_score(modified_vector)
                if keyword == domain_keyword:
                    contribution_score = max_score - calculate_max_correlation_score(modified_vector)[0]
                    contributing_words.append((word, contribution_score))

        contributing_words.sort(key=lambda x: x[1], reverse=True)
        return [word for word, _ in contributing_words]

    def get_overall_highest_correlating_domain(input_words):
        input_vector = np.zeros(glove_model.vector_size)

        for word in input_words:
            if word in glove_model:
                input_vector += glove_model[word]

        if np.any(input_vector):
            max_score, max_keyword = calculate_max_correlation_score(input_vector)
            return max_keyword
        else:
            return None

    overall_highest_correlating_domain = get_overall_highest_correlating_domain(input_words)
    contributing_words = get_contributing_words(input_words, overall_highest_correlating_domain)
    contributing_words = contributing_words[:30]
    contributing_words = set(contributing_words)
    return overall_highest_correlating_domain, contributing_words


def vmain2(lst,glove_model):
    user_comments = lst
    processed_comments = [preprocess_text(comment) for comment in user_comments]
    processed_comments = [comment for comment in processed_comments if len(comment) > 0]
    flattened_list_p_c = [item for sublist in processed_comments for item in sublist]
    dictionary = Dictionary(processed_comments)
    corpus = [dictionary.doc2bow(text) for text in processed_comments]
    num_topics = 10
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
    vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
    html_code = pyLDAvis.prepared_data_to_html(vis_data)
    dom,ml = identify_highest_correlating_domain(flattened_list_p_c,glove_model)
    # words_only_lists = [[word for word, _ in sublist] for sublist in ml]
    return html_code,dom,ml

# def vmain2(lst, glove_model):
#     user_comments = lst
#     processed_comments = [preprocess_text(comment) for comment in user_comments]
#     processed_comments = [comment for comment in processed_comments if len(comment) > 0]
#     flattened_list_p_c = [item for sublist in processed_comments for item in sublist]
#     dictionary = Dictionary(processed_comments)
#     corpus = [dictionary.doc2bow(text) for text in processed_comments]
#     num_topics = 10
#     lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
#     vis_data = gensimvis.prepare(lda_model, corpus, dictionary)

#     # Serialize vis_data to JSON
#     serialized_vis_data = json.dumps(vis_data, cls=gensimvis.JSONLDSerializableEncoder)

#     # Convert the serialized vis_data to HTML using pyLDAvis
#     html_code = pyLDAvis.prepared_data_to_html(serialized_vis_data)
#     dom, ml = identify_highest_correlating_domain(flattened_list_p_c, glove_model)
#     return html_code, dom, ml





