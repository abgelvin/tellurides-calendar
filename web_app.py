import os
from flask import Flask, request, render_template, session, Response
import mysql.connector
import sqlite3

from app import main

app = Flask(__name__)
app.secret_key = 'tellurides'


# Flask authentication
def check_auth(username, password):
    return username == os.getenv('USERNAME') and password == os.getenv('PASSWORD')


def authenticate():
    return Response('Could not verify username/password', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(function):
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return function(*args, **kwargs)
    return wrapper


@app.route('/', methods=['GET', 'POST'])
@requires_auth
def options():
    
    # Update database
    main()
    print('database updated')

    # Display schedule for selected date
    return display()
    
    ## Leaving this code in case it is taking too long to update db every time, then would use with layout.html
    # If method is GET, user has selected a date.  Retrieve info from the database.
    # if request.method == 'GET':
    #   return display()
    
    # If method is POST, update the database.
    # elif request.method == 'POST':
    #     main()
    #     return render_template('layout.html')

def display():
    
    # Create connection to planetscale database - original method
    # db = mysql.connector.connect(
    #     host=os.getenv('DB_HOST'), 
    #     user=os.getenv('DB_USER'),
    #     password=os.getenv('DB_PASSWORD'),
    #     db=os.getenv('DB_DB'),
    #     )

    # Create sqlite3 connection to avoid PlanetScale 
    db = sqlite3.connect('data.db')

    # Create cursor
    cu = db.cursor()

    # Get date from user
    session['date'] = str(request.args.get("date"))
    date = session['date']

    # Get db info for user selected date - '?' is '%s' for mysql
    rows = cu.execute('SELECT start_time, flight, ride_type, party, origin, destination, etx FROM reservations WHERE date = (?) ORDER BY start_time', (date,))
    rows = cu.fetchall()
    up = []
    down = []
    over = []
    
    # For each row separate into up, down, over lists
    for i in range(0, len(rows)):
        row = rows[i]
        if row[4] == 'MTJ' or row[4] == 'ATL':
            up.append(row)
        elif row[5] == "MTJ" or row[5] == 'ATL':
            down.append(row)
        else:
            over.append(row)
    session.clear()
    return render_template('layout2.html', date=date, up=up, down=down, over=over)



if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=3000)