# Installation:
## Python
- Make sure you have python installed
- - https://docs.python.org/3/using/windows.html#installation-steps

## Script install
- On windows, run the install.ps1 file by right clicking from file explorer and running with powershell
- On ubuntu, run the install.sh file 

## Manual installation
### Install pip
- Download: https://bootstrap.pypa.io/get-pip.py
- Windows: `py get-pip.py`
- Ubuntu: `python3 get-pip.py`
- Might need to run as admin

### Install python build
- Windows: `py -m pip install --upgrade build`
- Ubuntu: `python3 -m pip install --upgrade build`
- Might need to run as admin

### Install dependencies
- Pymunk: `pip install pymunk`
- Pygame: `pip install -U pygame --user`

## Install package
- Inside of the robot_sim folder run
- Windows: `py -m build`, Ubuntu: `python3 -m build`
- Windows: `pip install .`, Ubuntu: `pip install .`

# Running
Look at the example.py file provided for how to use
- Try running example.py to make sure it works