import os
#import jinja2
from flask import Flask, render_template
app = Flask(__name__)

#root = os.path.dirname(__file__)
#my_loader = jinja2.ChoiceLoader([
#        app.jinja_loader,
#        jinja2.FileSystemLoader([root])
#])
#app.jinja_loader = my_loader

@app.route("/<string:name>")
def page(name):
    return serve(name)

@app.route("/")
def home():
    return serve('index.html')


def serve(filename):
    return render_template(filename)

