import os
import json
from flask import Flask, render_template, redirect, abort
lunch = Flask(__name__)

@lunch.route("/")
def home():
    return 'Lunch'

