from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

import datetime
from dateutil.relativedelta import relativedelta
import os.path
import os
from dotenv import load_dotenv
import mysql.connector
import sqlite3

load_dotenv()
# SCOPES = os.getenv('SCOPES')
# print(f'SCOPES: {SCOPES}')
SCOPES = ['https://www.googleapis.com/auth/calendar']
GOOGLE_APPLICATION_CREDENTIALS = 'key_file.json'


def main():
    # Get events from google calendar API
    events = get_events()

    # Save retrieved events to database
    save_to_db(events)


def get_events():
    creds = None
    creds_path = 'key_file.json'

    # Establish credentials from key_file
    if os.path.exists(creds_path):
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)
        # print(f'scope: {SCOPES}')

    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # Call the calendar API and retrieve events for selected time period
        today = datetime.date.today()
        last_month = today + relativedelta(days=-1)
        next_month = today + relativedelta(months=+4)
        startDay = datetime.datetime.combine(last_month, datetime.datetime.min.time()).isoformat() + 'Z'
        endDay = datetime.datetime.combine(next_month, datetime.datetime.max.time()).isoformat() + 'Z'
        
        events_results =  service.events().list(calendarId='westernsloperides@gmail.com', 
                                            timeMin=startDay, timeMax=endDay, maxResults=2500, singleEvents=True, orderBy='startTime').execute()
        
        events = events_results.get('items', [])        
        print('events retrieved')

        if not events:
            return
        return events
    except HttpError as error:
        print(f'An http error occured: {error}')


def save_to_db(events):

    # Create connection with PlanetScale database
    # db = mysql.connector.connect(
    #     host = os.getenv('DB_HOST'),
    #     user = os.getenv('DB_USER'),
    #     password = os.getenv('DB_PASSWORD'),
    #     db = os.getenv('DB_DB')
    #     )

    # Create connection to local db file, avoiding PlanetScale
    db = sqlite3.connect('data.db')

    cu = db.cursor()

    # Create reservations table - 'AUTOINCREMENT' is 'AUTO_INCREMENT' for mysql
    cu.execute('CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT NOT NULL, start_time TEXT NOT NULL, flight TEXT NOT NULL, ride_type TEXT NOT NULL, party TEXT NOT NULL, origin TEXT NOT NULL, destination TEXT NOT NULL, etx TEXT NOT NULL)')

    # Clear database table of previous query data
    cu.execute('DELETE FROM reservations')

    # For each event from get_event(), retrieve the start date and summary
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        summary = event['summary']

        # Split the summary string at '-' to get the separate values and create list "fields"
        fields = summary.split('-')

        # If the first field of the summary is "cancelled," skip that event
        if fields[0] =='CANCELLED':
            continue
        
        try:

            # If there are at least 6 fields and there is a start time, retrieve fields from event and insert into db table
            if len(fields) > 5 and start:

                # Split datetime into date and time
                date_time = start.split('T')
                date = date_time[0]
                if len(date_time) < 2:
                    print(f'no date/time entered: {fields}')
                    continue
                start_time = date_time[1].split('-')[0]
                start_time = start_time[:len(start_time)-3]

                flight = fields[0]
                ride_type = fields[1]
                party = fields[2]
                origin = fields[3]
                destination = fields[4]
                etx = fields[5]

                # Add events to reservations database - '?' is '%s' for mysql
                cu.execute('INSERT INTO reservations (date, start_time, flight, ride_type, party, origin, destination, etx) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                           (date, start_time, flight, ride_type, party, origin, destination, etx,))

                db.commit()

        except Exception as e:
            print(f'An error occurred: {fields}')

            raise e
    print(f'saved to db')


if __name__ == '__main__':
    main()