# tellurides-calendar
application to retrieve and display TelluRides's reservations by date, this is the version that is used for onrender and planetscale
#### **Video Demo**:  https://youtu.be/mAm_GYTU4qU
#### Technologies and frameworks: Python, MySQL, Flask, HTML, CSS, bootstrap
#### **Description**
#### Purpose:
This is the version used for production

I have a friend that owns a shuttle company, primarily shuttling people from the airport to the resort town or vice versa.  The airport and resort are about 70 miles apart, so he has to coordinate his vans and drivers and know where everyone is at any given time.  He uses an app for reservations and backs that information up and organizes it in a google calendar.  Every morning he has to go through the reservations for the day and separate them into "up" (from the airport) and "down" (to the airport) trips.  If the trip is not to/from the airport, it is considered "over."  He wanted an app that could do this organization for him. This would save time each morning and also allow him to quickly see where the vehicles would be at a given time on a given day if someone called to make a reservation. 
#### Organization:
I thought it would be easiest to get information directly from the reservation application that he uses, but the company does not have a public API.  I decided to use the google calendar API and get the information directly from his google calendar, which he has copied and pasted from the reservation app.  Since I am new to APIs, there is also extensive documentation available on the google calendar API, which was invaluable.  
#### Files
- app.py
    - get_events: function that retrieves the events from the google calendar from today through a chosen  future date.  It takes the resulting event "summary" which is a string that is consisently [booking type]-[vehicle type]-[party name x number]-[origin]-[destination]-[misc info], and separates it at the '-' to create a list of the individual fields. 
    - save_to_db: function that inserts those fields into a 'reservation' table in a database with PlanetScale serverless MySQL platform. Before retrieving the data for a new date, the database table is cleared of previous entries.  
- web_app.py
    - check_auth: checks to see if username and password are valid
    - authenticate: returns error if check_auth returns false
    - requires_auth: wrapper to require authentication for given route
    - options: home route, requires authentication, calls main() to update the database, calls display() to retrieve data for date and display it
    - display: connects to platetscale database and retrieves data from "reservations" table, organizes it into "up" (origin is MTJ or ATL), "down" (destination is MTJ or ATL), "over" (all others)
   