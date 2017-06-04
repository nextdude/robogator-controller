#!/bin/bash

export FLASK_APP=app.py
export FLASK_DEBUG=1
FLASK_HOST=$(./get_ip.sh)
cd src
flask run --host=$FLASK_HOST
