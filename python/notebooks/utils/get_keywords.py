
# coding: utf-8

"""This script defines functions to extract RAKE and Textrank algo based keywords from any corpus file
Requires arguments to the corpus file (in CSV) and the column name for the story content"""
# In[20]:


import pandas as pd
from rake_nltk import Rake
import gensim.summarization as gs
import summa.keywords as sk
import traceback


# In[30]:


super_stopwords = nltk.corpus.stopwords.words("english")+['’']
raker = Rake(max_length=1, stopwords=super_stopwords)


# In[31]:


DATA_FILE = 'stories_content_english_corrected.csv'

# In[44]:


###
# RAKE keywords
###
def get_keywords_rake(csv_file_location=DATA_FILE, story_content_column_name='story_content'):
    data = pd.read_csv(csv_file_location)
    rake_keywords = []
    for story in data[story_content_column_name]:
        raker.extract_keywords_from_text(story)
        rake_keywords.append(raker.get_ranked_phrases())
    return rake_keywords


# In[45]:


####
# Textrank keywords
####

def get_keywords_textrank(csv_file_location=DATA_FILE, story_content_column_name='story_content', algo='summa'):
    data = pd.read_csv(csv_file_location)
    textrank_keywords = []
    for story in data[story_content_column_name]:
        # Get keywords from summa
        try:
            if algo == 'summa':
                textrank_keywords.append(sk.keywords(story).split('\n'))
            else if algo == 'gensim':
                textrank_keywords.append(gs.keywords(story).split('\n'))
            else:
                raise ValueError(algo + " is not a valid argument. Please choose between 'summa' & 'gesnim', which are currently supoorted")
        except Exception as e:
            print(algo + " has faced an exception in processing story: " + story)
            textrank_keywords.append([])
            traceback.print_exc()

    return textrank_keywords

