import lunch

def test_app():
    me = lunch.lunch.test_client()

    rv = me.get('/lunch/')
    assert b'<h1>Lunch</h1>' in rv.data


    rv = me.get('/lunch/register')
    assert b'Register' in rv.data


    rv = me.post('/lunch/register', data=dict(
        email='foo@bar..com'
    ))
    assert b'Invalid e-mail address' == rv.data


    email = 'foo@bar.com'
    rv = me.post('/lunch/register', data=dict(
        email=email
    ))
    assert b'sent' in rv.data

