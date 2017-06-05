#!/bin/bash

cd ~/robogator-controller
git pull
export FLASK_HOST=$(./get_ip.sh)
cd src
echo "Open http://${FLASK_HOST}:5000 in your browser"
python3 app.py
