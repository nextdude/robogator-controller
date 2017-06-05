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
    
def handle_action(req):
    res = { "action": req, "result": {"code": 0} }
    action = req['action'].pop(0)
    args = tuple(req['action'])
    if action == 'set_led':
        BP.set_led(args[0])
    return res

@app.route("/")
def index():
    return show_section('home')


@sockets.route("/gator")
def gator(ws):
    while True:
        req = json.loads(ws.receive())
        res = handle_action(req)
        ws.send(json.dumps(res))


@app.route("/<section>")
def show_section(section):
    if section not in ['home', 'think', 'walk', 'attack', 'color', 'jaws', 'help']:
        section = 'home'
    BP.reset_all();
    return render_template('{}.html'.format(section), section=section)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
