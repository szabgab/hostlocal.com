import os
import json
import re
import datetime
from flask import Flask, render_template, redirect, abort, Response
from flask_frozen import Freezer

app = Flask(__name__)

root = os.path.dirname( __file__ )

# @app.context_processor
# def inject_dates():
#     return dict(css_date = os.path.getmtime( os.path.join(root, 'static', 'style.css')))

@app.route("/robots.txt")
def robots():
    return Response('', mimetype='text/plain')

@app.route("/eng/")
@app.route("/heb/")
def no_listing():
    return redirect('/', code=302)

@app.route("/<any(eng, heb):lang>/<string:name>")
def eng_course(lang, name):
    if name.endswith('.html'):
        name = name[0:-5]
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
def show_page(name):
    app.logger.info(f"Trying to access '{name}'")
    if name in ['clients.html', 'gabor.html', 'perl.html', 'development.html', 'staff.html', 'contact.html', 'infrastructure.html']:
        return redirect('/', code=302)

    if name.endswith('.html'):
        name = name[0:-5]

    with open(os.path.join(root, 'pages.txt')) as fh:
        for row in fh:
            row = row.rstrip("\n")
            path, template_file, title = re.split(r"\s*;\s*", row)

            if name == path:
                app.logger.info(f"Trying to use template file '{template_file}'")
                return render_template(template_file,
                    page_title = title,
                )

    abort(404)


@app.route("/")
def home():
    schedule = read_schedule()
    return render_template('index.html',
        page_title = "Host Local Training courses for Rust and Python",
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
    return Response(xml, mimetype='application/xml')

def read_schedule(name = None):
    now = datetime.datetime.now()
    today = now.strftime('%Y.%m.%d')

    with open( os.path.join(root, 'schedule.json') ) as fh:
        schedule = json.load(fh)

    # remove old events
    schedule = list(filter(lambda event: event['date'] > today, schedule))

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


import glob
if __name__ == "__main__":
    app.config['FREEZER_DESTINATION'] = os.path.join(root, '_site')
    app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
    freezer = Freezer(app)

    @freezer.register_generator
    def eng_course():
        for lang in ['eng', 'heb']:
            for course in glob.glob(os.path.join(root, 'courses', lang, '*.json')):
                yield f"/{lang}/" + course.split('/')[-1][0:-5] + ".html"

    @freezer.register_generator
    def show_page():
        for name in ['clients.html', 'gabor.html', 'perl.html', 'development.html', 'staff.html', 'contact.html', 'infrastructure.html']:
            yield f"/{name}"


        for page in glob.glob(os.path.join(root, 'templates', '*.html')):
            name = page.split('/')[-1][0:-5]
            if name in ['index', 'image', 'course']:
                continue
            yield f"/{name}.html"

    freezer.freeze()
