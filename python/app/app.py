import unicodedata
from flask import Flask, render_template, request
import requests
import urllib
import re
from bs4 import BeautifulSoup


import os
import sys
sys.path.insert(0, os.getcwd())

from scripts.lda_model_loader import LdaModel
from scripts.get_story_illustration_text import get_illustration_text
from scripts.freq_word_extractor import get_freq_keywords


app = Flask(__name__)
PATH_LDA_MODEL_STORY_ONLY = os.path.abspath(os.path.join(os.getcwd(), "models/lda_model_stories_only"))
PATH_LDA_MODEL_STORY_AND_ILLUSTRATION = os.path.abspath(os.path.join(os.getcwd(), "models/lda_model_stories_and_illustration"))
API_URI = 'https://storyweaver.org.in/api/v1/'

LDA_MODEL_STORY_ONLY = LdaModel(MODEL_PATH=PATH_LDA_MODEL_STORY_ONLY)
LDA_MODEL_STORY_AND_ILLUSTRATION = LdaModel(MODEL_PATH=PATH_LDA_MODEL_STORY_AND_ILLUSTRATION)


@app.route('/', methods=['GET'])
@app.route('/<query>')
def index():
    if 'query' in request.args:
        q = request.args['query']
        if len(q.strip()) == 0:
            return render_template('index.html')
        story_path = urllib.parse.urlparse(q).path
        story_id = get_story_id(story_path)
        illustration_text = get_illustration_text(story_id)
        api_uri_path = get_api_path(story_path)
        pages_info = get_pages_info(requests.get(api_uri_path).json())
        tags = [
                {'model': 'LDA model with story text',
                 'tags': ', '.join(LDA_MODEL_STORY_ONLY.predict(pages_info['text_str']))},
                {'model': 'LDA model with story and illustration text',
                 'tags': ', '.join(LDA_MODEL_STORY_AND_ILLUSTRATION.predict(pages_info['text_str']+' '+illustration_text))},
                {'model': 'Frequency and Collations Model',
                 'tags': ', '.join(get_freq_keywords(pages_info['text_str']))}
             ]
        title = pages_info['title']
        img = pages_info['image_url']
        return render_template('index.html', tags=tags,
                               title=title,
                               img=img)
    return render_template('index.html')


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_pages_info(resp):
    '''Parse the request from the storyweaver api and get text of the story book
    '''
    pages = resp['data']['pages']
    parsed_info = {'texts': [],
                   'image_url': None,
                   'title': None}
    for page in pages:
        if page['pageType'] == 'FrontCoverPage':
            if parsed_info['image_url'] is None:
                parsed_info['image_url'] = page['coverImage']['sizes'][1]['url']
            if parsed_info['title'] is None:
                soup = BeautifulSoup(page['html'])
                title = soup.findAll("p", {"class": "cover_title"})[0].text
                parsed_info['title'] = title
        if page['pageType'] == 'StoryPage':
            cleantext = BeautifulSoup(page['html'], "lxml").text.replace('\n', ' ').replace('  ','')
            # remove unicode
            cleantext = unicodedata.normalize('NFKC', cleantext).replace('\"', '')
            parsed_info['texts'].append(cleantext)
    parsed_info['text_str'] = ' '.join(parsed_info['texts'])
    return parsed_info


def get_api_path(story_path):
    api_path = API_URI + story_path + '/read'
    return api_path

def get_story_id(story_path):
    last_slash_pos = story_path.rfind('/')+1
    return story_path[last_slash_pos:].split('-')[0]


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
