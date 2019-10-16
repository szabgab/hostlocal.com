import json
import sys
import os
from reportlab.pdfgen import canvas

pos_y = 800

def add_section(c, key, title, courses):
    global pos_y
    if key not in courses:
        exit("Missing {}".format(key))
    c.setFont("Helvetica", 20)
    c.drawString(20, pos_y, title)
    pos_y -= 20

    c.setFont("Helvetica", 12)
    for row in courses[key]:
        c.drawString(20, pos_y, row)
        pos_y -= 20
    pos_y -= 20


def main():
    global pos_y
    if len(sys.argv) != 2:
        exit("Usage {} courses/eng/a.json".format(sys.argv[0]))

    json_file = sys.argv[1]
    #print(json_file)
    pdf_file = os.path.basename(json_file[:-4] + 'pdf')
    with open(json_file) as fh:
        course = json.load(fh)

    c = canvas.Canvas(pdf_file)

    # TODO: fetch from canvas?
    full_x = 830
    full_y = 580

    c.setFont("Helvetica", 32)
    font_width = 26
    c.drawString(20, pos_y, "Training by Gabor Szabo")
    pos_y -= 40

    #pos_x = int((full_x - len(course["title"]) * font_width) / 2)
    pos_x = 20
    c.setFont("Helvetica", 30)
    c.drawString(pos_x, pos_y, course["title"])
    pos_y -= 40

    add_section(c, 'target_audience', 'Audience', course)
    add_section(c, 'objectives', 'Objectives', course)


    c.setFont("Helvetica", 14)
    c.drawString(60, 30, 'For more information visit https://hostlocal.com/   or call 054-4624648')

    #c.drawString(0, 830, "Here")  # top left corner
    #c.drawString(0, 0, "Zero")  # lower left corner
    c.showPage()
    c.save()

main()

