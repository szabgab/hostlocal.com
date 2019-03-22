from contextlib import contextmanager
import os
import json
import fcntl

# TODO flock!
@contextmanager
def database(db_file):
    if not os.path.exists(db_file):
        with open(db_file, 'w') as fh:
            default_data = {
                'users' : {},
            }
            json.dump(default_data, fh, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    with open(db_file, 'r+') as fh:
        fcntl.lockf(fh, fcntl.LOCK_EX)
        data = json.load(fh)
        try:
            yield data
        finally:
            fh.seek(0, 0)
            json.dump(data, fh, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

