from flask import Flask
from celery import Celery
from lib import functions

app = Flask(__name__)

@app.route('/')
def index():
    return 'POST to /recognize/(dining hall) with Clarifai outupt of an image or visit /test to test.'

'''
This route tests the preprocessing code and prints it to an output text file.
'''
@app.route('/test')
def test():
    return functions.preprocess(['Cuban Mojo Pork' , 'Fish Tilapia with Lemon Butter & Capers' , 'Herbed Grilled Turkey' ,'Spicy Black Bean Burger Patty'])

'''
Recognizes the closest match given a picture and the dining hall in a POST request.
Returns a json which contains the most likely matches and their likelyhoods.
Valid halls:
    busey-evans
    far
    ikenberry
    isr
    lar
    par
'''
@app.route('/recognize/<hall>/<meal>', methods=['POST'])
def recognize(hall, meal):
    valid_halls = {'busey-evans', 'far', 'ikenberry', 'isr', 'lar', 'par'}
    valid_meals = {'breakfast', 'lunch', 'dinner'}
    if hall not in valid_halls or meal not in valid_meals:
        return 'Invalid input'
    pass

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
