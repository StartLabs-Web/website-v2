from flask import Flask, render_template, url_for
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os
from dateutil import parser

app = Flask(__name__)

# For debugging only
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Index Page
@app.route('/')
def index():
    return render_template('index.html')


# Events Page
@app.route('/events')
def events():
    return render_template('events.html', events=getUpcomingEvents(5), getStringForEventTimeRange=getStringForEventTimeRange)

# Gets date range string from event
# i.e. 05 November 2018, 3:00 PM - 4:00 PM
def getStringForEventTimeRange(event):
    if 'date' in event['start']:
        # All day event
        start = datetime.datetime.strptime(event['start']['date'], "%Y-%m-%d")
        end = datetime.datetime.strptime(event['end']['date'], "%Y-%m-%d") - datetime.timedelta(days=1)
        if start.date() == end.date():
            # One day event
            return start.strftime("%d %B %Y")
        else:
            # One day event
            return start.strftime("%d %B %Y") + " – " + end.strftime("%d %B %Y")
    else:
        # Not all day event
        start = datetime.datetime.strptime(event['start']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(event['end']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")

        if start.date() == end.date():
            # One day event
            return start.strftime("%d %B %Y, %I:%M %p") + " – " + end.strftime("%I:%M %p")
        else:
            # One day event
            return start.strftime("%d %B %Y, %I:%M %p") + " – " + end.strftime("%d %B %Y, %I:%M %p")
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
    rootDir = os.path.dirname(os.path.abspath(__file__))
    store = file.Storage(os.path.join(rootDir, 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(rootDir, 'credentials.json'), SCOPES)
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
