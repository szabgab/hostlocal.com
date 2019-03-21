import lunch

def test_app():
    me = lunch.lunch.test_client()

    rv = me.get('/')
    assert b'Lunch' == rv.data


