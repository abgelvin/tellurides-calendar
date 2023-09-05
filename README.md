# tellurides-calendar
application to retrieve and display TelluRides's reservations by date

## files
- app.py 
    1. get_events: connects to google calendar API and retrieves events for given date range
    2. save_to_db: connects to planetscale database (wsr_db) and inserts retrieved google events into table
- web_app.py
    1. check_auth: checks to see if username and password are valid
    2. authenticate: returns error if check_auth returns false
    3. requires_auth: wrapper to require authentication for given route
    4. options: home route, requires authentication, calls main() to update the database, calls display() to retrieve data for date and display it
    5. display: connects to platetscale database and retrieves data from "reservations" table, organizes it into "up" (origin is MTJ or ATL), "down" (destination is MTJ or ATL), "over" (all others)
   