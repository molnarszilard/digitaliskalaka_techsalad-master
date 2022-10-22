from flask import Blueprint, render_template, request
from flask import session as login_session
from flask_login import login_required, current_user


from .models import Event, User, EventUsers
from . import db
import os
import requests

from io import BytesIO
import base64
import json
import time
import datetime
import io

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from PIL import Image

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/events/')
@login_required
def events():
    return render_template('events.html')

@main.route('/events/create')
@login_required
def events_create():
    return render_template('events_create.html')

@main.route('/events/list')
@login_required
def events_list():
    events = Event.query.all()
    return render_template('events_list.html', events=events)


@main.route('/checktrash')
@login_required
def checktrash():
    return render_template('checktrash.html', result={'label': 'empty'})

@main.route('/attend_event', methods=['POST'])
@login_required
def attend_event():
    json_obj = json.loads(request.data)
    event_id = json_obj['id']
    user_email = login_session['username']
    user = User.query.filter_by(email=user_email).first()
    # print(event_id, user.id)

    new_event_users = EventUsers(event_id=event_id, user_id=user.id)
    db.session.add(new_event_users)
    db.session.commit()

    event_users = EventUsers.query.all()
    for event_user in event_users:
        print(event_user.event_id, event_user.user_id)

    return "Event attendance accepted"

@main.route('/get_participants', methods=['POST'])
@login_required
def get_participants():
    json_obj = json.loads(request.data)
    event_id = json_obj['id']
    event_users = EventUsers.query.filter_by(event_id=event_id).all()
    final_users = []
    for event_user in event_users:
        new_user = User.query.filter_by(id=event_user.user_id).first()
        final_users.append(new_user)

    final_emails = list(map(lambda user: user.email, final_users))
    print(final_emails)
    return {'emails': final_emails }



@main.route('/create_event', methods=['POST'])
@login_required
def create_event():
    json_obj = json.loads(request.data)

    title = json_obj['title']
    description = json_obj['description']
    file = json_obj['bytes']
    dtime = json_obj['eventdate']
    longitude = json_obj['longitude']
    latitude = json_obj['latitude']

    # print(title, description, type(file), datetime)
    # print(login_session['username'])
    # print(longitude, latitude)

    organizator = User.query.filter_by(email=login_session['username']).first()

    # print(datetime.datetime.strptime(dtime, '%Y-%m-%dT%H:%M'))
    new_event = Event(title=title, description=description, datetime=datetime.datetime.strptime(dtime, '%Y-%m-%dT%H:%M'), 
                        latitude=latitude, longitude=longitude)

    starter = file.find(',')
    image_data = file[starter+1:]
    

    encoded = base64.b64decode(image_data)
    # print(encoded)
    new_path = './project/static/cashed_images/' + json_obj['name']
    with open(new_path, 'wb') as fh:
        fh.write(encoded)

    # new_event.image.from_blob(encoded)
    new_event.image_path = new_path
    new_event.image_name = json_obj['name']
    new_event.organizator_id = organizator.id
    new_event.organizator = organizator

    # add the new user to the database
    db.session.add(new_event)
    db.session.commit() 

    return "Event created"


@main.route('/check_trash', methods=['POST'])
@login_required
def check_trash():
    
    
    target = os.path.join(APP_ROOT, 'images/')
    

    if not os.path.isdir(target):
        os.mkdir(target)
    
    
    for file in request.files.getlist("file"):
        
        filename = file.filename

        destination = "/".join([target, filename])
        file.save(destination)

        my_img = {'image': open(destination, 'rb')}
        json_data={'filename':filename}
        r = requests.post("http://193.226.17.131:5001/classify",files=my_img,data=json_data)
        resp = r.json()
        
        print(resp)
        result=resp
    return render_template('checktrash.html', result=result)
