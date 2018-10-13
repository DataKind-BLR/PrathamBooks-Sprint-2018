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
from scripts.freq_word_extractor import get_freq_keywords


app = Flask(__name__)
MODEL = LdaModel()
API_URI = 'https://storyweaver.org.in/api/v1/'


@app.route('/', methods=['GET'])
@app.route('/<query>')
def index():
    if 'query' in request.args:
        q = request.args['query']
        if len(q.strip()) == 0:
            return render_template('index.html')
        story_path = urllib.parse.urlparse(q).path
        api_uri_path = get_api_path(story_path)
        pages_info = get_pages_info(requests.get(api_uri_path).json())
        tags = [{'model': 'LDA model',
                 'tags': ', '.join(MODEL.predict(pages_info['text_str']))},
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


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
