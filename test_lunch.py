import lunch

def test_app():
    me = lunch.lunch.test_client()

    rv = me.get('/lunch/')
    assert b'Lunch' == rv.data


