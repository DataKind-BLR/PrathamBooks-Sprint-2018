"""This script cleans the english data further which still has non-english stories
Output is a file called stories_content_english_corrected.csv"""

import pandas as pd
from nltk import RegexpTokenizer, WordNetLemmatizer, corpus

INPUT_FILE = 'stories_content_english.csv'
OUTPUT_FILE = 'stories_content_english_corrected.csv'
super_stopwords = corpus.stopwords.words("english")+['’']
lemmatizer = WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'[A-Za-z]+')


def preprocess_text(text):
    if type(text) != str:
        return []
    return [lemmatizer.lemmatize(w.lower()) for w in tokenizer.tokenize(text) if w.lower() not in super_stopwords]


data = pd.read_csv(INPUT_FILE)
# print(len(data))
#remove empty stories
english_data = data[data['story_content'].map(lambda x: preprocess_text(x)!=[] && type(x['story_id']) != str)]
non_english_data = data[data['story_content'].map(lambda x: preprocess_text(x)==[])]
# print(len(non_english_data))
# print(non_english_data)

english_data.to_csv(OUTPUT_FILE, index=False)

