import os
import json
from flask import Flask, render_template, redirect, abort
app = Flask(__name__)

root = os.path.dirname( __file__ )

@app.route("/robots.txt")
def robots():
    return ''

@app.route("/eng/")
def eng():
    return redirect('/', code=302)

@app.route("/eng/<string:name>")
def course(name):
    course_file = os.path.join(root, 'courses', 'eng', name + '.json')
    if os.path.exists(course_file):
        with open(course_file) as fh:
            course = json.load(fh)
        return render_template('course.html',
            course = course,
            page_title = "{} - Training course in Israel".format(course['title'])
        )
    abort(404)

@app.route("/<string:name>")
def page(name):
    if name in ['clients.html', 'gabor.html', 'perl.html', 'development.html', 'staff.html', 'contact.html', 'infrastructure.html']:
        return redirect('/', code=302)
    abort(404)


@app.route("/")
def home():
    return render_template('index.html',
        page_title = "Host Local Training courses for DevOps, in Git, Linux, Jenkins CI, Test Automation, Python",
    )

