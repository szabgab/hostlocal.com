import os
import json
from flask import Flask, render_template, redirect, abort
app = Flask(__name__)

root = os.path.dirname( __file__ )

@app.context_processor
def inject_dates():
    return dict(css_date = os.path.getmtime( os.path.join(root, 'static', 'style.css')))

@app.route("/robots.txt")
def robots():
    return ''

@app.route("/eng/")
@app.route("/heb/")
def no_listing():
    return redirect('/', code=302)

@app.route("/<any(eng, heb):lang>/<string:name>")
def eng_course(lang, name):
    course_file = os.path.join(root, 'courses', lang, name + '.json')
    schedule = read_schedule(name)
    if os.path.exists(course_file):
        with open(course_file) as fh:
            course = json.load(fh)
        return render_template('course.html',
            rtl        = (lang == 'heb'),
            course     = course,
            page_title = "{} - Training course in Israel".format(course['title']),
            schedule   = schedule,
            title      = read_titles(lang),
        )
    abort(404)


@app.route("/<string:name>")
def page(name):
    if name in ['clients.html', 'gabor.html', 'perl.html', 'development.html', 'staff.html', 'contact.html', 'infrastructure.html']:
        return redirect('/', code=302)
    abort(404)


@app.route("/consulting")
def consulting():
    return render_template('consulting.html',
        page_title = "Host Local Training courses for DevOps, in Git, Linux, Jenkins CI, Test Automation, Python",
    )

@app.route("/registration")
def consulting():
    return render_template('registration.html',
        page_title = "Registration to Training courses",
    )


@app.route("/")
def home():
    schedule = read_schedule()
    return render_template('index.html',
        page_title = "Host Local Training courses for DevOps, in Git, Linux, Jenkins CI, Test Automation, Python",
        schedule   = schedule,
    )


@app.route("/sitemap.xml")
def sitemap():
    xml = """
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://hostlocal.com/</loc>
    <lastmod>2019-03-10</lastmod>
  </url>
"""
    for course in os.listdir( os.path.join(root, 'courses', 'eng') ):
        xml += """
  <url>
    <loc>https://hostlocal.com/eng/{}</loc>
    <lastmod>2019-03-10</lastmod>
  </url>""".format(course[0:-5])

    xml += "\n</urlset>"
    return xml

def read_schedule(name = None):
    with open( os.path.join(root, 'schedule.json') ) as fh:
        schedule = json.load(fh)

    if name:
        schedule = list(filter(lambda event: event['course'] == name, schedule))

    for event in schedule:
        with open( os.path.join(root, 'courses', 'eng', event['course'] + '.json') ) as fh:
            course = json.load(fh)
            event['title'] = course['title']

    return schedule

def read_titles(name):
    with open(os.path.join(root, name + '.json')) as fh:
        return json.load(fh)

