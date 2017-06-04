#!/bin/bash

ifconfig wlan0 | grep "inet add" | awk '{print $2}' | awk -F: '{print $2}'
