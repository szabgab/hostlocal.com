import app

import os
import json

root = os.path.dirname( __file__ )

def test_app():
    me = app.app.test_client()

    rv = me.get('/')
    assert b'<div><a href="/">Host Local Training</a></div>' in rv.data


    rv = me.get('/clients.html')
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == 'http://localhost/'

    rv = me.get('/robots.txt')
    assert b'' == rv.data

    rv = me.get('/eng/other')
    assert rv.status == '404 NOT FOUND'
    #assert b'' == rv.data

    rv = me.get('/eng/')
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == 'http://localhost/'

def test_courses():
    for lang in ['eng', 'heb']:
        for course in os.listdir(os.path.join(root, 'courses', lang)):
            course_file = os.path.join(root, 'courses', lang, course)
            with open(course_file) as fh:
                course = json.load(fh)

