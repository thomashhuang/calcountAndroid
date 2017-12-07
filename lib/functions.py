import json
import urllib2
from clarifai.rest import ClarifaiApp
import retinasdk

clarifai_app = ClarifaiApp(api_key='ef5deeb1449d41629720e2177bdacb84')
food_model = clarifai_app.models.get('bd367be194cf45149e75f01d59f77ba7')
retina_client = retinasdk.LiteClient('5dfc0c20-a095-11e7-9586-f796ac0731fb')
shutterstock_auth = 'Basic ZjhlZDMtZjAzZDQtZWE5NmEtNTkxMWEtNzYyM2YtNjc4ZDc6OTVlMTktZmVlOTEtNjdmZjItYjIyYjItMzMwNDUtZjQyMTA='

'''
Given a list of food names in the form of strings, uses retinaSDK to process all of them and stores in a file and returns result as a string.
'''
def preprocess(menu_items):
    menu_file = open('processed_menu.txt', 'w')
    for item in menu_items:
        menu_file.write(item + ': ')
        best_descriptions = get_best_descriptions(item)
        menu_file.write(str(best_descriptions) + '\n')
    menu_file.close() 
    return 'Processed!'

'''
Given the name of a food item, creates and returns a dictionary of the best descriptions of the food.
'''
def get_best_descriptions(food_item):
    acceptance_threshhold = .5 #How certain a guess has to be to be considered a part of our final dict
    descriptions = dict()
    req = urllib2.Request('https://api.shutterstock.com/v2/images/search?per_page=5&query=' + food_item)
    req.add_header('Authorization', shutterstock_auth)
    response = json.loads(str(urllib2.urlopen(req).read()))
    '''
    if response['total_count'] == 0:
        keywords_of_food_item = retina_client.getKeywords(food_item)
        keywords_string = str()
        for word in keywords_of_food_item:
            keywords_string += word + ' '
        new_req = urllib2.Request('https://api.shutterstock.com/v2/images/search?per_page=8&query=' + keywords_string)
        new_req.add_header('Authorization', shutterstock_auth)
        response = json.loads(str(urllib2.urlopen(new_req).read()))
    '''
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


def compare():
    pass
