from apiclient import discovery  #.build
from oauth2client.service_account import ServiceAccountCredentials
import datetime
from dateutil.relativedelta import relativedelta
import os.path
import os
from dotenv import load_dotenv
import json



def main():
    # Get events from google calendar API
    events = get_events()

    # Save retrieved events to database
    save_to_db(events)


