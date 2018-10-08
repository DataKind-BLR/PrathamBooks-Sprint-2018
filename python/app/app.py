from flask import Flask, render_template, request
import requests
import urllib
import re
from bs4 import BeautifulSoup


import os
import sys
sys.path.insert(0, os.getcwd())

from scripts.lda_model_loader import LdaModel


app = Flask(__name__)
MODEL = LdaModel()
API_URI = 'https://storyweaver.org.in/api/v1/'


@app.route('/', methods=['GET'])
@app.route('/<query>')
def index():
    if 'query' in request.args:
        q = request.args['query']
        story_path = urllib.parse.urlparse(q).path
        api_uri_path = get_api_path(story_path)
        text = get_pages_text(requests.get(api_uri_path).json())
        tags = [{'model': 'LDA model',
                 'tags': ', '.join(MODEL.predict(text))}
                ]
        return render_template('index.html', tags=tags)
    return render_template('index.html')


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def get_pages_text(resp):
    '''Parse the request from the storyweaver api and get text of the story book
    '''
    pages = resp['data']['pages']
    texts = []
    for page in pages:
        cleantext = BeautifulSoup(page['html'], "lxml").text.replace('\n', ' ')
        texts.append(cleantext)
    return ' '.join(texts)


def get_api_path(story_path):
    api_path = API_URI + story_path + '/read'
    return api_path


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
