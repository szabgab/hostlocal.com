import os
import time
import json
import random
import string
import uuid
from validate_email import validate_email
from flask import Flask, render_template, redirect, abort, request
lunch = Flask(__name__)

from mydb import database


db_file = 'db.json'

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

    uid = str(uuid.uuid1())

    with database(db_file) as data:
        data['users'][uid] = {
            'email': email,
            'verify_code': code,
            'verify_code_timestamp': time.time(),
        }

    sendmail(email, code)
    return 'sent to ' + email

@lunch.route("/lunch/verify/<code>")
def verify(code):
    return 'verified'

def sendmail(to, code):
    pass



