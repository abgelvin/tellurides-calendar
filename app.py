from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

import datetime
from dateutil.relativedelta import relativedelta
import os.path
import os
# from dotenv import load_dotenv
import json
import mysql.connector


SCOPES = os.getenv('SCOPES')


def main():
    # Get events from google calendar API
    events = get_events()

    # Save retrieved events to database
    # save_to_db(events)


def get_events():
    creds = None
    creds_path = 'key_file.json'

    # Establish credentials from key_file
    if os.path.exists(creds_path):
        creds = service_account.Credentials.from_service_account_file(creds_path, scopes=SCOPES)

    try:
        service = build('calendar', 'v3', credentials=creds)
        print(f'service: {service}')
        # Call the calendar API and retrieve events for selected time period
        today = datetime.date.today()
        last_month = today + relativedelta(days=-1)
        next_month = today + relativedelta(months=+4)
        startDay = datetime.datetime.combine(last_month, datetime.datetime.min.time()).isoformat() + 'Z'
        endDay = datetime.datetime.combine(next_month, datetime.datetime.max.time()).isoformat() + 'Z'
        
        print('got this far')
        events_results =  service.events().list(calendarId='westernsloperides@gmail.com', 
                                            timeMin=startDay, timeMax=endDay, maxResults=2500, singleEvents=True, orderBy='startTime').execute()
        
        print('not this far')
        events = events_results.get('items', [])        
        print('events retrieved')

        if not events:
            return
        return events
    except HttpError as error:
        print(f'An http error occured: {error}')


def save_to_db(events):

    # Create connection with PlanetScale database
    db = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    db = os.getenv('DB_DB')
    )

cu = db.cursor()




if __name__ == '__main__':
    main()