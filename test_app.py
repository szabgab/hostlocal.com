import app

def test_app():
    me = app.app.test_client()
    rv = me.get('/')
    assert b'<div>Host Local Training</div>' in rv.data


    rv = me.get('/clients.html')
    assert rv.status == '302 FOUND'
    assert rv.headers['Location'] == 'http://localhost/'
