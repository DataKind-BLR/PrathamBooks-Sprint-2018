from flask import Flask, render_template, request

import os
import sys
sys.path.insert(0, os.getcwd())

from scripts.lda_model_loader import LdaModel


app = Flask(__name__)
MODEL = LdaModel()

@app.route('/', methods=['GET'])
@app.route('/<query>')
def index():
    print(request.args.get('query'))
    print(MODEL.predict('Elephant'))
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
