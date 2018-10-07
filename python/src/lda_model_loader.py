import nltk
import numpy as np
import os
from gensim.models import LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess, lemmatize


class LdaModel:

    """A class to load LDA model and predict the top keywords for a given story text"""

    __model = None
    __id2word_dictionary = None

    DEFAULT_MODEL_FILE_LOCATION = os.path.abspath(os.path.join(os.getcwd(), "../models/lda_model"))
    DEFAULT_DICTIONARY_FILE_LOCATION = os.path.abspath(os.path.join(os.getcwd(), "../../data/id2word_dictionary"))

    def __init__(self, MODEL_PATH=DEFAULT_MODEL_FILE_LOCATION, DICT_LOCATION=DEFAULT_DICTIONARY_FILE_LOCATION):
        self.__model = LdaMulticore.load(MODEL_PATH)
        self.__id2word_dictionary = Dictionary.load_from_text(DICT_LOCATION)
        print(self.__model)
        print(self.__id2word_dictionary)

    def _pos_tokenize_document(self, doc):
        tokens = simple_preprocess(doc)
        # lemmatizes, POS tags and remove stopwords (including empty strings) from the tokens list for stories
        pos_tokens = [lemmatize(t) for t in tokens if t not in STOPWORDS and len(t)>0]
        # flatten the list-of-lists of POS tokens created by previous operation and return
        return [word for inner_list in pos_tokens for word in inner_list]


    def _get_noun_and_adjective(self, doc):
        pos_tokens = self._pos_tokenize_document(doc)
        NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']
        ADJECTIVES = ['JJ', 'JJR', 'JJS']
        word_pos_tuples = [token.decode('utf-8').split('/') for token in pos_tokens]
        return_words = [word for word, pos in word_pos_tuples if pos in NOUNS+ADJECTIVES]
        return return_words

    def _get_top_n_words(self, prediction, n=10):
        word_to_proba = {}
        for topic_id, topic_proba in prediction:
            topic_words = self.__model.show_topic(topic_id)
            for word, word_proba in topic_words:
                if word not in word_to_proba:
                    word_to_proba[word] = 0
                word_to_proba[word] += topic_proba * word_proba
        ranked_words_and_prob = sorted(word_to_proba.items(), key=lambda kv: kv[1], reverse=True)
        ranked_words = [word_tuple[0] for word_tuple in ranked_words_and_prob]
        return ranked_words[:n]

    def _clean(self, doc_string):
        return self._get_noun_and_adjective(doc_string)

    def predict(self, doc_string):
        tokenized_doc = self._clean(doc_string)
        bow_representation = self.__id2word_dictionary.doc2bow(tokenized_doc)
        prediction = self.__model[bow_representation]
        return self._get_top_n_words(prediction, 10)
