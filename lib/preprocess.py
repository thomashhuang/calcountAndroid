from clarifai.rest import ClarifaiApp
import retinasdk

clarifaiApp = ClarifaiApp(api_key='ef5deeb1449d41629720e2177bdacb84')
retinaClient = retinasdk.LiteClient('5dfc0c20-a095-11e7-9586-f796ac0731fb')

'''
Given a list of food names in the form of strings, uses retinaSDK to process all of them and stores in a file.
Stored in the file in the following format:
    Pizza: [1, 2, 3, 5, 6, 7, ...]
    Pear: [7, 61, 71, 90, 94...]
    (Food Item): (retina fingerprint)(newline)
'''
def preprocess(menu_items):
    menu_string = ''
    menu_file = open('processed_menu.txt', 'w')
    for item in menu_items:
        menu_file.write((item + ': '))
        menu_string += (item + ': ')
        fingerprint = retinaClient.getFingerprint(item)
        menu_file.write((str(fingerprint) + '\n'))
        menu_string += (str(fingerprint) + '\n')
    menu_file.close()
    return menu_string

