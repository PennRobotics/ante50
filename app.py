from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('index.html', round_num='5')
    return render_template('index.html', round_num='1')

