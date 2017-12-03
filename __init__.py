from flask import Flask
from lib import preprocess

app = Flask(__name__)

@app.route('/')
def index():
    return 'POST to /recognize with a link to the image or visit /test to test.'

'''
This route will run the recognition logic on a preset image.
'''
@app.route('/test')
def test():
    return preprocess.preprocess(['Apple', 'Pear', 'Tomato'])

if __name__ == '__main__':
    app.run()
