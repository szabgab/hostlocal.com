import app

def test_app():
    me = app.app.test_client()
    rv = me.get('/')
    assert b'<div>Host Local Training</div>' in rv.data
