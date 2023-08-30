from flask import Flask, request, render_template, redirect, make_response

from app import main

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def options():

    # If method is GET, user has selected a date.  Retrieve info from the database.
    if request.method == 'GET':
        return display()
    
    # If method is POST, update the database.
    elif request.method == 'POST':
        main()
        return render_template('layout.html')