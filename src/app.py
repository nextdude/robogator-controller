""" +-----------------------------------------------------
    | Robogator Controller Application
    |
    | By Krishna Lyons
    | 6th Grade Full Year Project - Burke Middle School
    | Washington, DC
    +------------------------------------------------------ 
"""
from flask import Flask, render_template, redirect, url_for
from flask_sockets import Sockets
import brickpi3
import time
import json

BP = brickpi3.BrickPi3()
app = Flask(__name__)
sockets = Sockets(app)

@app.route("/")
def index():
    return show_section('home')

@sockets.route("/gator")
def gator(ws):
    while True:
        msg = ws.receive()
        info = { "Incoming":msg, "Manufacturer":BP.get_manufacturer(), "Board":BP.get_board(), "Serial Number":BP.get_id(), "Hardware version":BP.get_version_hardware(), "Firmware version":BP.get_version_firmware(), "Battery voltage":BP.get_voltage_battery(), "9v voltage":BP.get_voltage_9v(), "5v voltage":BP.get_voltage_5v(), "3.3v voltage":BP.get_voltage_3v3() }
        ws.send(json.dumps(info))

@app.route("/<section>")
def show_section(section):
    if section not in ['home','wink','walk','attack','color','jaws','help']:
        section = 'home'
    return render_template('{}.html'.format(section), section=section)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
