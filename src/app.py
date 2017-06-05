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

def init_scenario(scenario):
    err = None
    return err

def handle_scenario_action(req):
    res = { "status": "ok" }
    if req['action'] == 'stop':
        BP.reset_all()
        res['status'] = 'scenario-done'
    if req['action'] == 'start':
        err = init_scenario(req['scenario'])
        if err is not None:
            res.status = "error"
            res.error = err
        else:
            res.status = 'scenario-ready'
    return res

@app.route("/")
def index():
    return show_section('home')


@sockets.route("/gator")
def gator(ws):
    while True:
        req = json.loads(ws.receive())
        res = handle_scenario_action(req)
        ws.send(json.dumps(res))


@app.route("/<section>")
def show_section(section):
    if section not in ['home', 'think', 'walk', 'attack', 'color', 'jaws', 'help']:
        section = 'home'
    return render_template('{}.html'.format(section), section=section)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
