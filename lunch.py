import os
import time
import json
import random
import string
import yaml
from validate_email import validate_email
from flask import Flask, render_template, redirect, abort, request, Response
lunch = Flask(__name__)
from pymongo import MongoClient

@lunch.route("/")
def root():
    return redirect('/lunch')


@lunch.route("/lunch/")
def home():
    return render_template('lunch/index.html')


@lunch.route("/lunch/register", methods=['GET', 'POST'])
def register():
    email = request.form.get('email')
    if not email:
        return render_template('lunch/register.html')

    if not validate_email(email):
        return "Invalid e-mail address"

    code = str(int(time.time())) + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))

    db = get_db()
    entry = {
            'email': email,
            'verify_code': code,
            'verify_code_timestamp': time.time(),
    }
    db.people.insert_one(entry)
    sendmail(email, code)
    return 'sent to ' + email

@lunch.route("/lunch/verify/<code>")
def verify(code):
    return 'verified'

@lunch.route("/lunch/profile")
def profile():
    abort(401)

def sendmail(to, code):
    pass

#@lunch.errorhandler(401)
#def custom_401(error):
#    return Response('Need to login first.', 401, {})

def get_db():
    config_file = os.environ.get('LUNCH_CONFIG_FILE')
    if not config_file:
        root = os.path.dirname(os.path.dirname(__file__))
        config_file = os.path.join(root, "config.yml")
    print(config_file)
    with open(config_file) as fh:
        config = yaml.load(fh)
    if config["username"] and config["password"]:
        connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])
    else:
        connector = "mongodb://{}".format(config["server"])
    client = MongoClient(connector)
    return(client[config['dbname']])

