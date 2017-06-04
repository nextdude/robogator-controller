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

app = Flask(__name__)
sockets = Sockets(app)

@app.route("/")
def index():
    return show_section('home')

@app.route("/<section>")
def show_section(section):
    if section not in ['home','move','proximity','color','poke','help']:
        section = 'home'
    return render_template('{}.html'.format(section))

@sockets.route("/gator-brain")
def gator_brain(ws):
    while not ws.closed:
      msg = ws.receive()
      print('received {}'.format(msg))
      ws.send(msg)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
