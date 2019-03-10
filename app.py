import os
from flask import Flask, render_template, redirect
app = Flask(__name__)

@app.route("/robots.txt")
def robots():
    return ''

@app.route("/<string:name>")
def page(name):
    if name in ['clients.html', 'gabor.html', 'perl.html', 'development.html', 'staff.html', 'contact.html', 'infrastructure.html']:
        return redirect('/', code=302)

@app.route("/")
def home():
    return render_template('index.html')

