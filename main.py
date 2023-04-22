#!/usr/bin/python3
"""
This module Utilizes basic routes and simple
html display and utilizes render_template
which allows rendering of external reference html
files
"""
from flask import Flask, escape, render_template, request
import os

from final_model_text import detectAilment

os.environ["FLASK_APP"] = "main.py"

# Function that creates the app


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_school():
    """ Function returns a very basic html string without any tags"""
    return render_template('diagnosis.html', result=None)


@app.route('/diagnosis', strict_slashes=False, methods=['POST','GET'])
def int_display_template():
    """ param num:
                    must be a string value.
        description:
                    Interprets sting Values on a
                    templates file
    """
    symptom  = request.form['symptom']
    diagnosis = detectAilment(symptom)
    # print("You are suffering from :", diagnosis)
    return render_template('diagnosis.html', result=diagnosis)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
