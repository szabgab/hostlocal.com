#!/usr/bin/env python
import argparse
import re
import os
import sys
import json
import shutil

# convert my JSON format to the pseudo-XML format used by Brend
# 300px × 225px  for the IMAGE and
# 130px × 70px for the THUMBNAIL

outdir = 'xml'

# ABSTRACT - appears on the page listing the courses https://www.bodenseo.com/courses.php?topic=Python
#          - also the top of the course page: https://www.bodenseo.com/course/python_training_course.html
# DETAILS  - on the page of the course
# SLOGAN, SLOGAN2 - on the left hand side of the page

def main():
    args = get_args()
    if os.path.exists(outdir):
        for filename in os.listdir(outdir):
            os.unlink( os.path.join(outdir, filename) )
    else:
        os.mkdir(outdir)
    #if len(sys.argv) < 2:
    #    exit(f"Usage: {sys.argv[0]} FILENAMEs")
    #print(args.files)
    for filename in args.files:
        convert(args, filename)
    os.system("tar czf xml.tar.gz xml/");

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('files',  help="filenames(s)", nargs="+")
    args = parser.parse_args()
    return args

def convert(args, infile):
    outfile = os.path.join(outdir, re.sub(r'\.json', '.xml', os.path.basename(infile)))
    template = get_template()

    with open(infile) as fh:
        data = json.load(fh)
    if args.strict:
        for key in ['title', 'text', 'keywords', 'target_audience']:
            if key not in data:
                print(f"{infile} missing {key}")

    template = re.sub(r'\{\{LANGUAGE}}',         'en', template)
    template = re.sub(r'\{\{MAINTITLE}}',        'Python Courses:', template)
    template = re.sub(r'\{\{TITLE}}',            data['title'], template)
    template = re.sub(r'\{\{ABSTRACT}}',         '\n'.join(data.get('text', [])), template)
    template = re.sub(r'\{\{KEYWORDS}}',         ', '.join(data.get('keywords', [])), template)
    template = re.sub(r'\{\{SLOGAN}}',           '', template)
    template = re.sub(r'\{\{SLOGAN2}}',          '', template)
    template = re.sub(r'\{\{METADESCRIPTION}}',  '', template)
    template = re.sub(r'\{\{COST}}',             '', template)
    template = re.sub(r'\{\{TARGET}}',           '\n'.join(data['target_audience']), template)

    template = re.sub(r'\{\{THUMBNAIL}}',        data['pic130'], template)
    template = re.sub(r'\{\{THUMBNAIL-TXT}}',    data['pic130_text'], template)
    template = re.sub(r'\{\{IMAGE}}',            data['pic300'], template)
    template = re.sub(r'\{\{IMAGE-TXT}}',        data['pic300_text'], template)

    for filename in [data['pic130'], data['pic300']]:
        shutil.copyfile( os.path.join('static', filename), os.path.join( outdir, filename) )

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
{{THUMBNAIL}}
</THUMBNAIL>
<THUMBNAIL-TXT>
{{THUMBNAIL-TXT}}
</THUMBNAIL-TXT>
<IMAGE>
{{IMAGE}}
</IMAGE>
<IMAGE-TXT>
{{IMAGE-TXT}}
</IMAGE-TXT>
'''


main()

