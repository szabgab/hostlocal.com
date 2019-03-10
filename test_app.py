import app

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

