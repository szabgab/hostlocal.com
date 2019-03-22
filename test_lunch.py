import lunch
import os

_to = None
_code = None

def _capture_mail(to, code):
    global _to
    global _code
    _to = to
    _code = code

lunch.sendmail = _capture_mail

def test_app(tmpdir):
    tdir = str(tmpdir)
    print(tdir)
    lunch.db_file = os.path.join(tdir, 'test_db.json')

    me = lunch.lunch.test_client()

    rv = me.get('/lunch/')
    assert b'<h1>Lunch</h1>' in rv.data


    rv = me.get('/lunch/register')
    assert b'Register' in rv.data


    rv = me.post('/lunch/register', data=dict(
        email='foo@bar..com'
    ))
    assert b'Invalid e-mail address' == rv.data


   # TODO test that we remove spaces and make the e-mail lowercase


    email = 'foo@bar.com'
    rv = me.post('/lunch/register', data=dict(
        email=email
    ))
    assert b'sent' in rv.data
    assert email == _to
    print(_code)

    rv = me.get('/lunch/verify/' + _code)
    assert b'verified' in rv.data


   # TODO: check that we send out an e-mail with a unique code in a link to be clicked
   # TODO: click on the link to make the e-mail verified and give access to the site
