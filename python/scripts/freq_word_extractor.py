from collections import Counter
from nltk import ngrams
from nltk.tokenize import wordpunct_tokenize
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder


STOP_WORDS = set(stopwords.words('english'))


def get_ngrams(tokens, n):
    return [' '.join(list(words)) for words in list(ngrams(tokens, n))]


def clean_and_tokenize_text(text):
    # remove punctuations, lower and tokenize the text
    stripped = wordpunct_tokenize(text.lower())
    [STOP_WORDS.add(word) for word in ['said', 'says',
                                       'saying', 'ask',
                                       'asking', 'like',
                                       'say']]
    words = [word for word in stripped if word.isalpha() and word not in STOP_WORDS]
    return words


def get_best_keywords(text):
    # pick top n based on distance from the max frequency
    words_df = pd.DataFrame(get_top_k_n_words(text, 20), columns=['word', 'freq'])
    words_df['normalized_freq'] = words_df.apply(lambda x: x.freq + len(x.word.split()), axis=1)
    words_df['z_score'] = (words_df.normalized_freq - words_df.normalized_freq.mean()) / words_df.normalized_freq.std(ddof=0)
    return list(words_df[words_df.z_score > 1].word.values)


def get_top_k_n_words(text, k=5, n=2):
    tokens = clean_and_tokenize_text(text)
    ngrams = get_ngrams(tokens, n)
    freq = Counter(tokens + ngrams)
    return freq.most_common(k)


def get_top_bigrams(text, n):
    bigram_measures = BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(clean_and_tokenize_text(text))
    finder.apply_freq_filter(2)
    return [' '.join(list(words)) for words in finder.nbest(bigram_measures.raw_freq, n)]


def get_freq_keywords(text):
    collocations = get_top_bigrams(text, 5)
    freq = [word for word, freq in get_top_k_n_words(text, 10)]
    combined_tags = set(collocations + freq)
    return [word for word in list(combined_tags) if len(word) > 3][:10]
