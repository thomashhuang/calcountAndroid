from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'POST to /recognize with a link to the image or visit /test to test.'

'''
Making a post request to this route will run the recognition script with the link to the given image.
For now, it returns based on a hard-coded link.
'''
@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'GET':
        return 'Make a POST request to this URL to process.'
    elif request.method == 'POST':
        link_to_image = request.data
        if True: #Set to True when testing to use a hard-coded image link.
            link_to_image = 'http://2.bp.blogspot.com/_LOn5giboI0Q/TCrA_r7b7gI/AAAAAAAAELA/vzPzmtKgY14/s1600/IMG_1117.JPG'
        return render_template('ImageRecognition.html', link = link_to_image)

'''
This route will run the recognition logic on a preset image.
'''
@app.route('/test')
def test():
    return render_template('ImageRecognitionTest.html', index = 0)

if __name__ == '__main__':
    app.run()
