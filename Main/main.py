from flask import Flask, render_template, url_for
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os

app = Flask(__name__)

# Define CSS colors here!
colors = {}
colors["upper_logo"] = "rgb(13, 133, 77)"
colors["navbar_nonactive"] = "rgb(13, 133, 77)"
colors["navbar_active"] = "rgb(48, 211, 70)"

# Redesign
@app.route('/')
def home():
    return render_template("home.html", colors=colors)

@app.route('/about')
def about():
    return render_template("about.html", colors=colors)

@app.route('/events')
def events():
    return render_template("events.html", colors=colors)

@app.route('/partners')
def partners():
    return render_template("partners.html", colors=colors)

@app.route('/team')
def team():
    return render_template("team.html", colors=colors)

@app.route('/contact')
def contact():
    return render_template("contact.html", colors=colors)


def get_team_headshots():
    # Get headshots
    filepaths = os.listdir("static/old/images/2018-members")
    filepaths = ["old/images/2018-members/" + f for f in filepaths]
    headshots_paths = []
    for f in filepaths:
        if "white" in f:
            headshots_paths.append(f)


# num_future_events = 5
# num_past_events = 3


# # Index Page
# @app.route('/new')
# def new_version():
#     # Get headshots
#     filepaths = os.listdir("static/old/images/2018-members")
#     filepaths = ["old/images/2018-members/" + f for f in filepaths]
#     headshots_paths = []
#     for f in filepaths:
#         if "white" in f:
#             headshots_paths.append(f)
#     return render_template('index.html', events=getUpcomingEvents(num_future_events, num_past_events),
#     getStringForEventTimeRange=getStringForEventTimeRange, headshots=headshots_paths)


# # Google Calendar API

# # Gets date range string from event
# # i.e. 05 November 2018, 3:00 PM - 4:00 PM
# def getStringForEventTimeRange(event):
#     if 'date' in event['start']:
#         # All day event
#         start = datetime.datetime.strptime(event['start']['date'], "%Y-%m-%d")
#         end = datetime.datetime.strptime(event['end']['date'], "%Y-%m-%d") - datetime.timedelta(days=1)
#         if start.date() == end.date():
#             # One day event
#             return start.strftime("%d %B %Y")
#         else:
#             # Multiple day event
#             return start.strftime("%d %B %Y") + " - " + end.strftime("%d %B %Y")
#     else:
#         # Not all day event
#         start = datetime.datetime.strptime(event['start']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
#         end = datetime.datetime.strptime(event['end']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")

#         if start.date() == end.date():
#             # One day event
#             return start.strftime("%d %B %Y, %I:%M %p") + " - " + end.strftime("%I:%M %p")
#         else:
#             # Multiple day event
#             return start.strftime("%d %B %Y, %I:%M %p") + " - " + end.strftime("%d %B %Y, %I:%M %p")

# # Gets events from google calendar
# # Returns array of specified length or total number of upcoming events
# # Based on https://developers.google.com/calendar/quickstart/python
# def getUpcomingEvents(num_future, num_past):
#     # indicates readonly access to calendar api
#     SCOPES = 'https://www.googeeleapis.com/auth/calendar.readonly'
#     # id of startlabs calendar
#     calendarId = 'startlabs.management@gmail.com'
#     # for debugging only, use to test without changing active startlabs calendar
#     # calendarId = 'e5bo6318kog0sq0u66tqpqn5l4@group.calendar.google.com'

#     # Authentication using Google CalendarAPi
#     rootDir = os.path.dirname(os.path.abspath(__file__))
#     store = file.Storage(os.path.join(rootDir, 'token.json'))
#     creds = store.get()
#     if not creds or creds.invalid:
#         flow = client.flow_from_clientsecrets(os.path.join(rootDir, 'credentials.json'), SCOPES)
#         creds = tools.run_flow(flow, store)
#     service = build('calendar', 'v3', http=creds.authorize(Http()))

#     # Call the Calendar API and fetch events
#     now = datetime.datetime.now().isoformat() + 'Z' # 'Z' indicates UTC time
#     events_result = service.events().list(calendarId=calendarId, timeMin=now,
#                                         maxResults=num_future, singleEvents=True,
#                                         orderBy='startTime').execute()
#     future_events = events_result.get('items', [])

#     events_result = service.events().list(calendarId=calendarId, timeMax=now,
#                                         singleEvents=True, orderBy='startTime').execute()
#     past_events = events_result.get('items', [])
#     past_events = past_events[len(past_events)-num_past:]
#     events = past_events + future_events
#     return events

if __name__ == '__main__':
    app.run(debug=True)
