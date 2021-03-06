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
    
def handle_actions(req):
    res = { "actions": req['actions'], "result": {"code": 0, "values": []} }
    for action in req['actions']:
        method = action[0]
        args = action[1:]
        if method == 'set_led':
            BP.set_led(*args)
            time.sleep(0.01)
        elif method == 'sleep':
            time.sleep(*args)
        elif method == 'set_motor_power':
            BP.set_motor_power(*args)
        elif method == 'set_sensor_type':
            BP.set_sensor_type(*args)
        elif method == 'get_sensor':
            try:
                value = BP.get_sensor(*args)
            except brickpi3.SensorError as error:
                print(error)
                value = 255
            res['result']['values'].append(value)
    return res

@app.route("/")
def index():
    return show_section('home')


@sockets.route("/gator")
def gator(ws):
    while True:
        req = json.loads(ws.receive())
        res = handle_actions(req)
        ws.send(json.dumps(res))


@app.route("/<section>")
def show_section(section):
    if section not in ['home', 'think', 'walk', 'attack', 'color', 'jaws']:
        section = 'home'
    BP.reset_all();
    return render_template('{}.html'.format(section), section=section)


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
