#!/bin/sh
sudo apt install python3-pip
python3 -m pip install --upgrade build
python3 -m pip install -U pygame --user
python3 -m build
python3 -m pip install .
