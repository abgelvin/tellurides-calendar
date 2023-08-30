from flask import Flask, make_response


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def options