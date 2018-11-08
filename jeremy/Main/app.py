from flask import Flask, render_template
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

app = Flask(__name__)

# Index Page
@app.route('/')
def index():
    return render_template('index.html')

# Events Page
@app.route('/events')
def events():
    return render_template('events.html', events=getUpcomingEvents(5))

# Gets events from google calendar
# Returns array of specified length or total number of upcoming events
# Based on https://developers.google.com/calendar/quickstart/python
def getUpcomingEvents(num_events):
    # indicates readonly access to calendar api
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    # id of startlabs calendar
    # calendarId = 'startlabs.management@gmail.com'
    # temporarily using other calendar because startlabs one is empty :(
    calendarId = 'e5bo6318kog0sq0u66tqpqn5l4@group.calendar.google.com'

    # Authentication
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API and fetch events
    now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=calendarId, timeMin=now,
                                        maxResults=num_events, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events
    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

if __name__ == '__main__':
    app.run(debug=True)
