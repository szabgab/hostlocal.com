import os
import json
from validate_email import validate_email
from flask import Flask, render_template, redirect, abort, request
lunch = Flask(__name__)

@lunch.route("/")
def root():
    return redirect('/lunch')


@lunch.route("/lunch/")
def home():
    return render_template('lunch/index.html')


@lunch.route("/lunch/register", methods=['GET', 'POST'])
def register():
    email = request.form.get('email')
    if email:
        if validate_email(email):
            return 'sent to ' + email
        else:
            return "Invalid e-mail address"
    return render_template('lunch/register.html')

