# tellurides-calendar
application to retrieve and display TelluRides's reservations by date

## files
- app.py 
    1. get_events: connects to google calendar API and retrieves events for given date range
    2. save_to_db: connects to planetscale database (wsr_db) and inserts retrieved google events into table
- web_app.py
    1. display: connects to platetscale database and retrieves data from "reservations" table, organizes it into "up" (origin is MTJ or ATL), "down" (destination is MTJ or ATL), "over" (all others)
    2. options: if request method is "GET" (choosing a date to retrieve schedule), call display to show schedule; if request method is "POST" (repopulating database), call main from app.py