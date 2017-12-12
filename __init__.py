from flask import Flask, request, jsonify
from lib import functions
import json

app = Flask(__name__)

@app.route('/')
def index():
    return 'POST to /recognize/(dining hall)/(meal) with Clarifai outupt of an image or visit /test to test.'

'''
This route runs the preprocessing code on the list of items. The results of processing are then stored in a text file corresponding to the hall and meal.
'''
@app.route('/process')
def process():
    functions.preprocess(['Fruit Tray', 'Makanek', 'Smoked Tofu Steak Mango Chutney', 'Lemon Dill Chicken Breast', 'Korean Miso Soup', 'Tuscan Soup', 'Cobb Salad', 'Tuscan Orzo Salad', 'Sliced Garlic Bread', 'Braised Red Cabbage', 'Green Beans', 'Jasmine Rice', 'Gemelli Pasta', 'Marinara Sauce', 'Creamy Pesto Sauce', 'Dutch Apple Pie'], 'isr', 'dinner')
    return 'Processed!'

'''
This route tests the preprocessing code, outputs to a text file, then returns the contents of that file.
'''
@app.route('/test')
def test():
    functions.preprocess(['Cuban Mojo Pork' , 'Halal Baked Chicken w/ BBQ Sauce' , 'Herbed Grilled Turkey' ,'Spicy Black Bean Burger Patty'])
    return open('menus/test_menu.txt', 'r').read()

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
Valid meals:
    breakfast
    lunch
    dinner
'''
@app.route('/recognize/<hall>/<meal>', methods=['POST'])
def recognize(hall, meal):
    valid_halls = {'busey-evans', 'far', 'ikenberry', 'isr', 'lar', 'par'}
    valid_meals = {'breakfast', 'lunch', 'dinner'}
    if hall not in valid_halls or meal not in valid_meals:
        return 'Invalid input'
    request_data = json.loads(request.data)
    description = request_data['description']
    match_list = functions.recognize(description, hall, meal)
    return jsonify(matches=match_list)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
