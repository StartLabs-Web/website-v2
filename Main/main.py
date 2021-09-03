from flask import Flask, render_template, url_for
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os, csv

import chardet

try:
    __import__(mailing_list_info)
except:
    mailing_list_name = None
    mailing_list_password = None

app = Flask(__name__)

#####################
# Define CSS colors #
#####################
# first layer (DO NOT USE THESE IN THE HTML/CSS)
base = {}
base["dark"] = "rgb(9, 0, 134)" #dark blue
base["medium"] = "rgb(228, 0, 124)" #neon pink
base["light"] = "rgb(255, 203, 0)" #yellow 
base["accent_one"] = "rgb(69, 92, 255)" #blue
base["accent_two"] = "rgb(146, 1, 119)" #dark pink

# second layer (USE THESE IN THE HTML/CSS)
colors = {}
colors["dark"] = base["dark"]
colors["medium"] = base["medium"]
colors["light"] = base["light"]
colors["accent_one"] = base["accent_one"]
colors["accent_two"] = base["accent_two"]

colors["navbar_nonactive"] = base["dark"]
colors["navbar_active"] = base["medium"]
colors["h1"] = base["dark"]
colors["h2"] = base["medium"]
colors["h3"] = base["accent_one"]
colors["link"] = base["light"]
colors["contact_button"] = base["medium"]
colors["footer"] = base["dark"]
colors["minititle"] = base["medium"]


# 
#########
# Links #
#########
@app.route('/')
def home():
    return render_template("home.html", page="home", colors=colors, events=getUpcomingEvents(num_total_events, num_future_events),
        getTimeStringForEvent=getTimeStringForEvent, getDateStringForEvent=getDateStringForEvent, getShortDescription=getShortDescription, isPast=isPast)

@app.route('/about')
def about():
    return render_template("about.html", page="about", colors=colors)

@app.route('/test')
def test():
    return render_template("mailing-list.html")

@app.route('/add_to_mailing_list', methods=['POST'])
def add_to_mailing_list():
    addMemberToMailingList(request.form['email'])

@app.route('/events')
def events():
    # return render_template("construction.html", page="events", colors=colors)
    return render_template("large_events.html", page="events", colors=colors)

@app.route('/partners')
def partners():
    return render_template("partners.html", page="partners", colors=colors)

@app.route('/team')
def team():
    headshots_info = get_headshots_info()
    return render_template("team.html", page="team", colors=colors, team_headshots_info = get_team_data(), exec_headshots_info = get_exec_data())

@app.route('/contact')
def contact():
    return render_template("contact.html", page="contact", colors=colors)

@app.route('/entrepalooza')
def entrepalooza():
    return render_template("entrepalooza.html", page="entrepalooza", colors=colors)

@app.route('/apply')
def recruitment():
    return render_template("recruitment.html", page="apply", colors=colors)


# @app.route('/ideafactory')
# def ideafactory():
#     return render_template("ideafactory.html", page="ideafactory", colors=colors) 


#############
# Headshots #
#############
"""
A sample entry of 'all_data':
    OrderedDict([
        ('Timestamp', '2021/10/11 9:17:32 AM AST'), 
        ('Name', 'Isaac Lau'), 
        ('Graduation Year', '2022'), 
        ('Major', '6-2 Minor in 2; EECS with a Minor in MechE'), 
        ('Department', 'Large Events'), 
        ('Blurb', "As a moonshot engineer, I seek to push the boundaries of human capablities in speed and control through the power of autonomy and I am most interested in the interplay between mechanical and electrical systems.  If I'm not working on p-sets, catch me on campus working on the Hyperloop pod or find me in a machine shop!  "), ('image_path', '/static/images/anon-face.png')
    ])       
"""
def get_team_data():
    # Get filepaths of existing imgs
    existing_filenames = os.listdir(os.path.join(app.static_folder, 'images/2021-team'))
    # print(existing_filenames)
    # Read the csv file
    filename = os.path.join(app.static_folder, 'TeamBios2021.csv')
    # Build up the all_data list 
    all_data = []
    with open(filename, encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            # Set the image_path
            # If the image exists, give it an image from 2021-team, otherwise give it anon-face
            fullname = row["Name"]
            firstname, lastname = fullname.split(" ")
            
            # Below is what we used to use with white background images
            # possible_img_name = firstname.lower() + "-white.jpg"

            possible_img_name = firstname.lower() + lastname.lower() + ".jpg"
            if (possible_img_name in existing_filenames):
                possible_img_path = "images/2021-team/" + firstname.lower() + lastname.lower() + ".jpg"
                row["image_path"] = possible_img_path
                # row["image_path"] = url_for('static', filename=possible_img_path)
            else:
                row["image_path"] = 'images/anon-face.png'
                # row["image_path"] = '/static/images/anon-face.png'
            # print(row)
            all_data.append(row)
    all_data.sort(key=lambda x: x['Name'].split()[-1])
    # For debugging:
    # for row in all_data:
    #     print('row: ', row)
    return all_data

def get_exec_data():
    # Get filepaths of existing imgs
    existing_filenames = os.listdir(os.path.join(app.static_folder, 'images/2021-exec'))
    # print(existing_filenames)
    # Read the csv file
    filename = os.path.join(app.static_folder, 'ExecBios2021.csv')
    # Build up the all_data list 
    all_data = []
    with open(filename, encoding = "ISO-8859-1") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        for row in csv_reader:
            # Set the image_path
            # If the image exists, give it an image from 2021-team, otherwise give it anon-face
            fullname = row["Name"]
            firstname, lastname = fullname.split(" ")
            
            # Below is what we used to use with white background images
            # possible_img_name = firstname.lower() + "-white.jpg"

            possible_img_name = firstname.lower() + lastname.lower() + ".jpg"
            if (possible_img_name in existing_filenames):
                possible_img_path = "images/2021-exec/" + firstname.lower() + lastname.lower() + ".jpg"
                row["image_path"] = possible_img_path
                # row["image_path"] = url_for('static', filename=possible_img_path)
            else:
                row["image_path"] = 'images/anon-face.png'
                # row["image_path"] = '/static/images/anon-face.png'
            # print(row)
            all_data.append(row)
    # For debugging:
    # for row in all_data:
    #     print('row: ', row)
    return all_data
            
"""
Purpose: Get photos and info about team member headshots
Params:  None
Returns: a list of dictionaries, with each dict holding information about one team member
Example:
[
    {'path': '/static/images/2018-members/leon-white.jpg', 'filename': 'leon-white.jpg', 'firstname': 'leon'},
    {'path': '/static/images/2018-members/matthew-white.jpg', 'filename': 'matthew-white.jpg', 'firstname': 'matthew'}
]
"""
def get_headshots_info():
    file_paths = get_headshots_filepaths()
    # only accept photos with 'white'
    headshots_paths = []
    for f in file_paths:
        # if "white" in f:
            headshots_paths.append(f)
    # turn into a list of dictionary
    headshots_info = []
    for path in headshots_paths:
        d = dict()
        d["path"] = path
        d["filename"] = d["path"].split("/")[-1]
        d["firstname"] = d["filename"].split("-")[0]
        headshots_info.append(d)
    # Also add those people without facial pictures taken
    remaining_names = [
        "Adriano Hernandez",
        "Alex Gu",
        "Alex Quach",
        "Allen Wang",
        "Ally Hong",
        "Amanda Garofalo",
        "Amber Lu",
        "Anj Fayemi",
        "Anjali Chadha",
        "Anjali Singh",
        "Anton Morgunov",
        "Anurag Golla",
        "Avichal Goel",
        "Brendan Ashworth",
        "Caleb Harris",
        "Daniela Velez",
        "Dev Patale",
        "Eileen Pan",
        "GiMin Choi",
        "Hannah Kim",
        "Isaac Lau",
        "Isaac Toscano",
        "Ishana Shastri",
        "Jamie Fu",
        "Jennifer Pan",
        "Jeremy McCulloch",
        "Jessica Sonner",
        "Katherine Wang",
        "Kendyll Hicks",
        "Lilian Wang",
        "Lucy McMillan",
        "Neha Hulkund",
        "Nitya Parthasarathy",
        "Raunak Chowdhury",
        "Ruben Castro",
        "Sarah Moseson",
        "Sathya Peri",
        "Saumya Rawat",
        "Shayna Ahteck",
        "Shobhita Sundaram",
        "Shruti Ravikumar",
        "Sophie Van Pelt",
        "Spencer Toll",
        "Sreya Vengara",
        "Thomas Ngo",
        "Ting Li",
        "Tobi Mustapha",
        "Wilson Spearman",
    ]
    # remaining_names = sorted(remaining_names)
    for name in remaining_names:
        d = dict()
        d["path"] = '/static/images/anon-face.png'
        d["filename"] = "n/a"
        d["firstname"] = name
        headshots_info.append(d)
    return headshots_info

"""
Purpose: Retreive all filepaths to files located in "static/images/2018-members"
Params:  None
Returns: (list of strings) all the filepaths to the headshot photos
"""
def get_headshots_filepaths():
    file_paths = []
    # find the absolute path to the folder, then list folder contents
    filenames = os.listdir(os.path.join(app.static_folder, 'images/2021-team'))
    # make the path relative to location of 'static' folder
    for i in range(len(filenames)):
        tmp_path = os.path.join('images/2021-team/', filenames[i])
        file_paths.append(url_for('static', filename=tmp_path))
    return file_paths

#######################
# Google Calendar API #
#######################

num_total_events = 3
num_future_events = 2
description_length_chars = 140

def addMemberToMailingList(email):
    if mailing_list_name != None:
        os.system("/mit/consult/bin/mmblanche " + mailing_list_name + " -p " + mailing_list_password + " -a " + email)

def isPast(event):
    if 'date' in event['start']:
        end = datetime.datetime.strptime(event['end']['date'], "%Y-%m-%d")
    else:
        end = datetime.datetime.strptime(event['end']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
    return end < datetime.datetime.now()


def getShortDescription(description):
    if description != None and len(description) > description_length_chars:
        description = description[0:description_length_chars]
        description = description[0:description.rfind(' ')]
        description = description + "..."
    return description
# Gets date range string from event
# i.e. 05 November 2018, 3:00 PM - 4:00 PM
def getTimeStringForEvent(event):
    if 'date' not in event['start']:
        start = datetime.datetime.strptime(event['start']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(event['end']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
        if start.date() == end.date():
            # All day event
            return start.strftime("%I:%M %p") + " - " + end.strftime("%I:%M %p")
        else:
            return None
    else:
        return None

def getDateStringForEvent(event):
    if 'date' in event['start']:
        # All day event
        start = datetime.datetime.strptime(event['start']['date'], "%Y-%m-%d")
        end = datetime.datetime.strptime(event['end']['date'], "%Y-%m-%d") - datetime.timedelta(days=1)
    else:
        # Not all day event
        start = datetime.datetime.strptime(event['start']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(event['end']['dateTime'][:-6], "%Y-%m-%dT%H:%M:%S")

    if start.date() == end.date():
        # One day event
        return start.strftime("%d %B %Y")
    else:
        # Multiple day event
        return start.strftime("%d %B %Y") + " - " + end.strftime("%d %B %Y")

# Gets events from google calendar
# Returns array of specified length or total number of upcoming events
# Based on https://developers.google.com/calendar/quickstart/python
def getUpcomingEvents(num_total, num_future):
    # indicates readonly access to calendar api
    SCOPES = 'https://www.googeeleapis.com/auth/calendar.readonly'
    # id of startlabs calendar
    calendarId = 'startlabs.management@gmail.com'
    # for debugging only, use to test without changing active startlabs calendar
    # calendarId = 'e5bo6318kog0sq0u66tqpqn5l4@group.calendar.google.com'

    # Authentication using Google CalendarAPi
    rootDir = os.path.dirname(os.path.abspath(__file__))
    print(rootDir)
    store = file.Storage(os.path.join(rootDir, 'token.json'))
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.join(rootDir, 'credentials.json'), SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API and fetch events
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=calendarId, timeMin=now,
                                        maxResults=num_future, singleEvents=True,
                                        orderBy='startTime').execute()
    future_events = events_result.get('items', [])

    num_past = num_total - len(future_events)

    events_result = service.events().list(calendarId=calendarId, timeMax=now,
                                        singleEvents=True, orderBy='startTime').execute()
    past_events = events_result.get('items', [])
    past_events = [event for event in past_events if event not in future_events]
    past_events = past_events[len(past_events)-num_past:]
    events = past_events + future_events
    return events

if __name__ == '__main__':
    app.run(debug=True)
