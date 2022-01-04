#!/bin/sh
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
python3 -m pip install --upgrade build
python3 -m pip install -U pygame --user
python3 -m build
python3 -m pip install .
