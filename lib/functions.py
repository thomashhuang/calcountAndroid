import json
import urllib2
from clarifai.rest import ClarifaiApp
import retinasdk

clarifai_app = ClarifaiApp(api_key='ef5deeb1449d41629720e2177bdacb84')
food_model = clarifai_app.models.get('bd367be194cf45149e75f01d59f77ba7')
retina_client = retinasdk.LiteClient('5dfc0c20-a095-11e7-9586-f796ac0731fb')
shutterstock_auth = 'Basic ZjhlZDMtZjAzZDQtZWE5NmEtNTkxMWEtNzYyM2YtNjc4ZDc6OTVlMTktZmVlOTEtNjdmZjItYjIyYjItMzMwNDUtZjQyMTA='

'''
Given a list of foods and the hall and meal, stores clarifai descriptions in a text file.
When testing, stores in a file called 'test_menu.txt'
'''
def preprocess(menu_items, hall = 'test', meal = 'menu'):
    menu_file = open('menus/' + hall + '_' + meal + '.txt', 'w')
    for item in menu_items:
        menu_file.write(item + ': ')
        best_descriptions = get_best_descriptions(item)
        description_string = ''
        keywords = retina_client.getKeywords(item)
        for key in best_descriptions.keys():
            description_string += str(key) + ' '
        for word in keywords:
            description_string += word + ' '
        for keyword in retina_client.getKeywords(description_string):
            menu_file.write(keyword + ' ')
        menu_file.write('\n')
    menu_file.close()

'''
Given the name of a food item, creates and returns a dictionary of the best descriptions of the food.
'''
def get_best_descriptions(food_item):
    acceptance_threshhold = .5 #How certain a guess has to be to be considered a part of our final dict
    descriptions = dict()
    important_words = retina_client.getKeywords(food_item)
    search_words = str()
    for word in important_words:
        search_words += word + ' '
    req = urllib2.Request('https://api.shutterstock.com/v2/images/search?per_page=4&query=' + search_words)
    req.add_header('Authorization', shutterstock_auth)
    r = urllib2.urlopen(req).read()
    response = json.loads(str(r))
    if response['total_count'] == 0:
        return None
    num_pictures = 0
    for picture in response['data']:
        num_pictures += 1
        item_url = picture['assets']['preview']['url']
        clarifai_output = food_model.predict_by_url(url=item_url)
        for guess in clarifai_output['outputs'][0]['data']['concepts']:
            if guess['name'] not in descriptions:
                descriptions[guess['name']] = guess['value']
            else:
                descriptions[guess['name']] += guess['value']
    for key in descriptions.keys():
        descriptions[key] /= num_pictures
        if descriptions[key] < acceptance_threshhold:
            descriptions.pop(key)
    return descriptions

'''
Given a string which contains clarifai output of a picture, compares it with the menu items
of the given hall and meal. Returns the top five results with the top being most likely.
'''
def recognize(description, hall, meal):
    menu = open('menus/' + hall + '_' + meal + '.txt', 'r')
    matches = dict()
    line = menu.read_line()
    while line:
        food_item = line[0:index(':')]
        match_value = retina_client.compare(description, line[index(':') + 2 : -1])
        matches[match_value] = food_item
        line = menu.read_line()
    possibility_list = list()
    for probability in sorted(matches):
        possibility_list.insert(0, matches[probability])
    if len(possibility_list > 5):
        return possibility_list[:5]
    return possibility_list
