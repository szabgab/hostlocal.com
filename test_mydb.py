from mydb import database
import os

def test_db(tmpdir):
    tdir = str(tmpdir)
    print(tdir)
    db_file = os.path.join(tdir, 'test_my_db.json')
    with database(db_file) as data1:
        assert data1 == {
                'users' : {},
            }
        data1['name'] = 'Foo Bar'

    with database(db_file) as data2:
        assert data2 == {
                'users' : {},
                'name':  'Foo Bar',
            }

        data2['users']['123'] = {
            'name': 'Hello World',
        }

    with database(db_file) as data3:
        assert data3 == {
                'users' : {
                    '123': {
                        'name': 'Hello World',
                    },
                },
                'name':  'Foo Bar',
            }

