
# coding: utf-8

# In[3]:


import pandas as pd
import nltk
import math


# In[2]:


ENGLISH_ONLY_STORIES_FILE = 'stories_content_english_corrected.csv'
TAGS_FILE = 'stories_tags.csv'


# In[7]:


def is_english(word):
    return word in nltk.corpus.words.words()

def is_single_word(word):
    return word.find(' ') == -1


def get_tags(story_file=ENGLISH_ONLY_STORIES_FILE, tag_file=TAGS_FILE):
    story_data = pd.read_csv(ENGLISH_ONLY_STORIES_FILE)
    tag_data = pd.read_csv(TAGS_FILE)
    pub_stories = story_data.loc[story_data['story_publishing_type'] == 'Publisher Story']
    pub_story_ids = pub_stories['story_id'].tolist()
    pub_tag_data = tag_data.loc[tag_data['story_id'].isin(pub_story_ids)]
    
    single_word_tags = set()
    story_tag_dict = {}
    
    for i, row in pub_tag_data.iterrows():
        tag = row['story_tag_name']
        if type(tag) == float and math.isnan(tag):
            continue
        if row['story_title'] not in story_tag_dict:
            story_tag_dict[row['story_title']] = []

        if is_english(tag) and is_single_word(tag):
            story_tag_dict[row['story_title']].append(tag.lower())
            single_word_tags.add(tag.lower())

    return single_word_tags

