from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello!'

@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'GET':
        return 'Upload a file to this URL to process.'
    # image = Image.open(request.files['file'])
    image = request.data

@app.route('/retinasdk')
def retinasdk():
    return render_template('retina-sdk-1.0.min.js')

@app.route('/test')
def test():
    return render_template('ImageRecognition.html', link = 0)

if __name__ == '__main__':
    app.run()
