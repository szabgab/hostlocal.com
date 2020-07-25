#!/usr/bin/env python3
import json
import glob

# format the json files

def tidy(filename):
    with open(filename) as fh:
        data = json.load(fh)
    with open(filename, 'w') as fh:
        json.dump(data, fh, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)

for filename in glob.glob("courses/eng/*.json"):
    try:
        tidy(filename)
    except Exception as err:
        print(f"Failed for {filename}")
        print(err)

# vim: expandtab
