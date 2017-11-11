from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'POST to /recognize with a link to the image or visit /test to test.'

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'GET':
        return 'Upload a file to this URL to process.'
    elif request.method == 'POST':
        link_to_image = request.data
        return render_template('ImageRecognition.html', link = link_to_image)

@app.route('/test')
def test():
    return render_template('ImageRecognition.html', link = 0)

if __name__ == '__main__':
    app.run()
