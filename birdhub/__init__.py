import os
from pydoc import cli

from flask import Flask, flash, redirect, request
from . import db

from paho.mqtt import client

HOST = "test.mosquitto.org"
mqtt = client.Client()

def on_publish(client,userdata,mid):
    print("User", str(userdata), "has published something")
    pass

mqtt.subscribe("birdhub/loadCell/+")



mqtt.connect(HOST,1883,60)
mqtt.subscribe("birdhub/loadCell/+")
mqtt.subscribe("birdhub/loadCell")

mqtt.on_publish = on_publish

# starting listening for messages
mqtt.loop_start()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'birdhub.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    db.init_app(app)
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')
        
    return app