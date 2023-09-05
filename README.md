# tellurides-calendar
application to retrieve and display TelluRides's reservations by date

## files
- app.py 
    - get_events: connects to google calendar API and retrieves events for given date range
    - save_to_db: connects to planetscale database (wsr_db) and inserts retrieved google events into table
- web_app.py
    - check_auth: checks to see if username and password are valid
    - authenticate: returns error if check_auth returns false
    - requires_auth: wrapper to require authentication for given route
    - options: home route, requires authentication, calls main() to update the database, calls display() to retrieve data for date and display it
    - display: connects to platetscale database and retrieves data from "reservations" table, organizes it into "up" (origin is MTJ or ATL), "down" (destination is MTJ or ATL), "over" (all others)
   