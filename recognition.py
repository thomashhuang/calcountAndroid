from flask import Flask, request
# from PIL import Image

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello!'

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'GET':
        return 'Upload a file to this URL to process.'
    # image = Image.open(request.files['file'])
    imgae = request.data
