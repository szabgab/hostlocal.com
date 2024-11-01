import app

import os
import json

root = os.path.dirname( __file__ )

def test_app():
    me = app.app.test_client()

    rv = me.get('/')
    assert rv.status == '200 OK'
    assert b'<div><a href="/">Host Local Training</a></div>' in rv.data
    assert b'<h2>Previous clients</h2>' in rv.data
    assert b'<h2 id="about-gabor">About Gabor Szabo</h2>' in rv.data
    assert b'2020.10.20' not in rv.data # old course
    assert rv.content_type == 'text/html; charset=utf-8'

    rv = me.get('/consulting')
    assert rv.status == '200 OK'
    #print(rv.data)
    assert b'<div><a href="/">Host Local Training</a></div>' in rv.data
    assert b'<title>Host Local Training courses for DevOps, in Git, Linux, Jenkins CI, Test Automation, Python</title>' in rv.data
    assert rv.content_type == 'text/html; charset=utf-8'

    rv = me.get('/registration')
    assert rv.status == '200 OK'
    #print(rv.data)
    assert b'<div><a href="/">Host Local Training</a></div>' in rv.data
    assert b'<title>Registration to Training courses</title>' in rv.data
    assert rv.content_type == 'text/html; charset=utf-8'



    rv = me.get('/clients.html')
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == '/'
    assert rv.content_type == 'text/html; charset=utf-8'

    rv = me.get('/robots.txt')
    assert rv.status == '200 OK'
    assert b'' == rv.data
    assert rv.content_type == 'text/plain; charset=utf-8'

    rv = me.get('/sitemap.xml')
    assert rv.status == '200 OK'
    # TODO: check the content
    assert rv.content_type == 'application/xml; charset=utf-8'

    rv = me.get('/eng/rust')
    assert rv.status == '200 OK'
    # TODO: check the content
    assert rv.content_type == 'text/html; charset=utf-8'


    rv = me.get('/eng/other')
    assert rv.status == '404 NOT FOUND'
    assert rv.content_type == 'text/html; charset=utf-8'
    #assert b'' == rv.data

    rv = me.get('/eng/')
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == '/'
    assert rv.content_type == 'text/html; charset=utf-8'





def test_courses():
    for lang in ['eng', 'heb']:
        for course in os.listdir(os.path.join(root, 'courses', lang)):
            course_file = os.path.join(root, 'courses', lang, course)
            with open(course_file) as fh:
                course = json.load(fh)

