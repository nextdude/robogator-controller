""" +-----------------------------------------------------
    | Robogator Controller Application
    |
    | By Krishna Lyons
    | 6th Grade Full Year Project - Burke Middle School
    | Washington, DC
    +------------------------------------------------------ 
"""
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    """ Doc string here """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
