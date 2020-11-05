#!/usr/bin/env python
import argparse
import re
import os
import sys
import json

# convert my JSON format to the pseudo-XML format used by Brend
# 300px × 225px  for the IMAGE and
# 130px × 70px for the THUMBNAIL

def main():
    args = get_args()
    #if len(sys.argv) < 2:
    #    exit(f"Usage: {sys.argv[0]} FILENAMEs")
    print(args.files)
    for filename in args.files:
        convert(filename)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files',  help="filenames(s)", nargs="+")
    args = parser.parse_args()
    return args

def convert(infile):
    outfile = re.sub(r'\.json', '.xml', os.path.basename(infile))
    template = get_template()

    with open(infile) as fh:
        data = json.load(fh)
    template = re.sub(r'\{\{LANGUAGE}}',         'en', template)
    template = re.sub(r'\{\{MAINTITLE}}',        'Python Courses:', template)
    template = re.sub(r'\{\{TITLE}}',            data['title'], template)
    template = re.sub(r'\{\{ABSTRACT}}',         '\n'.join(data['text']), template)
    template = re.sub(r'\{\{KEYWORDS}}',         ', '.join(data['keywords']), template)
    template = re.sub(r'\{\{SLOGAN}}',           '', template)
    template = re.sub(r'\{\{SLOGAN2}}',          '', template)
    template = re.sub(r'\{\{METADESCRIPTION}}',  '', template)
    template = re.sub(r'\{\{COST}}',             '', template)
    template = re.sub(r'\{\{TARGET}}',           '\n'.join(data['target_audience']), template)

    details = ''
    for part in data['syllabus']:
        details += part['title'] + '\n'
        details += '<ul>\n'
        for row in part['entries']:
            details += '<li>' + row + '</li>\n'
        details += '</ul>\n'
    template = re.sub(r'\{\{DETAILS}}',          details, template)
    with open(outfile, 'w') as fh:
        fh.write(template)
    #print(template)
    #print(data.keys())



def get_template():
    return '''<LANGUAGE>
{{LANGUAGE}}
</LANGUAGE>
<TITLE>
{{TITLE}}
</TITLE>
<MAINTITLE>
{{MAINTITLE}}
</MAINTITLE>
<SECTION>
Python
</SECTION>
<ABSTRACT>
{{ABSTRACT}}
</ABSTRACT>
<KEYWORDS>
{{KEYWORDS}}
</KEYWORDS>
<METADESCRIPTION>
{{METADESCRIPTION}}
</METADESCRIPTION>
<SLOGAN>
{{SLOGAN}}
</SLOGAN>
<SLOGAN2>
{{SLOGAN2}}
</SLOGAN2>
<TARGET>
{{TARGET}}
</TARGET>
<PRICE_GROUP>
medium
</PRICE_GROUP>
<COSTS>
{{COST}}
</COSTS>
<DETAILS>
{{DETAILS}}
Of course, we can tailor this course to meet
your specific goals.  Please, don't hesitate to contact us.
</DETAILS>
<ADDITIONAL>
Comprehensive material
</ADDITIONAL>
<THUMBNAIL>
green_python130.png
</THUMBNAIL>
<THUMBNAIL-TXT>
Green Tree Python, Public Domain, excerpt from original image from pixabay.com
</THUMBNAIL-TXT>
<IMAGE>
green_python.png
</IMAGE>
<IMAGE-TXT>
Green Tree Python, Public Domain, original from pixabay.com
</IMAGE-TXT>
'''


main()

