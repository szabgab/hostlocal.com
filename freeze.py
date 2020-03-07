from flask_frozen import Freezer
from app import app
import os

app.config.update(
    FREEZER_DESTINATION = 'docs',
    FREEZER_IGNORE_MIMETYPE_WARNINGS = True,
)

freezer = Freezer(app)

courses = []

for lang in os.listdir('courses'):
    for filename in os.listdir( os.path.join('courses', lang)  ):
        if not filename.endswith('.json'):
            continue
        courses.append({
            'lang': lang,
            'name': filename[0:-5],
        })
print(courses)

@freezer.register_generator
def eng_course():
    for course in courses:
        yield course


if __name__ == '__main__':
    freezer.freeze()
