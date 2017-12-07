from flask import Flask
from lib import functions

app = Flask(__name__)

@app.route('/')
def index():
    return 'POST to /recognize with a link to the image or visit /test to test.'

'''
This route will return the retinaSDK fingerprints of some preset items.
'''
@app.route('/test')
def test():
    return functions.preprocess(['Sliced Chicken' , 'Miso Soup', 'Sliced Pineapple' , 'Egg Patty'])

if __name__ == '__main__':
    app.run()
