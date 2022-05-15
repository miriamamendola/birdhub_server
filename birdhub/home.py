from django.shortcuts import render
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from birdhub.db import get_db

bp = Blueprint('home', __name__)
from . import mqtt

def on_message(client, userdata, message):
    print("[" + str(message.topic) + "]:" +  message.payload.decode("utf-8"))
    
    if message.payload.decode("utf-8") == 'PlaceWeight':
        print("Redirecting")
        return redirect('/flash')

mqtt.on_message = on_message

@bp.route('/flash')
def flash():
    print("aaaa")
    return render_template('base.html')

@bp.route('/tare')
def tare():
    mqtt.publish("birdhub/loadCell/tare", "tare")
    return render_template('base.html')

#TODO 
@bp.route('/calibrate/', methods=('GET', 'POST'))
def get_known_weight():
    known_weight = request.form['known-weight']
    return redirect(known_weight)

#TODO 
@bp.route('/calibrate/ready')
def send_ready():
    mqtt.publish("birdhub/loadCell/calibration", 'ACK')
    return render_template('base.html')

@bp.route('/calibrate/<known_weight>', methods=('GET', 'POST'))
def start_calibration(known_weight):
    mqtt.publish("birdhub/loadCell/calibration", known_weight)
    return render_template('base.html')

@bp.route('/replenish/<supply>')
def replenish(supply):
    mqtt.publish("birdhub/replenish", supply)
    return render_template('base.html')

@bp.route('/setCheckTime/<time>')
def set_check_time(time):
    mqtt.publish("birdhub/setCheckTime", str(time))
    return render_template('base.html')

@bp.route('/setCheckTime/', methods=('GET', 'POST'))
def get_check_time():
    time = request.form['check-time']
    return redirect(time)

@bp.route('/setPumpTime/<time>')
def set_pump_time(time):
    mqtt.publish("birdhub/setPumpTime", str(time))
    return render_template('base.html')

@bp.route('/setPumpTime/', methods=('GET', 'POST'))
def get_pump_time():
    time = request.form['pump-time']
    return redirect(time)

@bp.route('/cam', methods=('GET', 'POST'))
def get_data():
    if request.method == 'POST':
        print(request.data)
        base_name = "bird"
        db = get_db()
        
        last_id = db.execute(
            'SELECT p.photo_id FROM photo p ORDER BY p.photo_id DESC LIMIT 1'
        ).fetchone()
        print(last_id)

        photo_name = '/images/' + base_name + str(last_id[0]).zfill(3) + ".jpg"
        with open('./birdhub/static' + photo_name, 'wb') as file:
            file.write(request.data)

        db.execute(
            'INSERT INTO photo (photo_name) VALUES(?)',
            (photo_name,)
        )
        
        db.commit()
    return 'Got data'




def get_last_photo():
    return get_db().execute(
            'SELECT p.photo_name FROM photo p ORDER BY p.photo_id DESC LIMIT 1'
        ).fetchone()
    

@bp.route('/takePicture')
def take_photo():
    mqtt.publish("birdhub/cam", "photo")
    return render_template('base.html')

@bp.route('/')
def index():
    photo_name = get_last_photo()
    return render_template('base.html', photo=photo_name)


""" @bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
 """
