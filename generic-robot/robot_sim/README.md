# Installation:
## Python
- Make sure you have python installed
- - https://www.python.org/downloads/windows/

## Script install
- On windows, run the install.ps1 file by right clicking from file explorer and running with powershell
- On ubuntu, run the install.sh file 

## Manual installation
### Install python build
- Windows: `py -m pip install --upgrade build`
- Ubuntu: `python3 -m pip install --upgrade build`

### Install dependencies
- Pymunk: `py -m pip install pymunk`
- Pygame: `py -m pip install -U pygame --user`

## Install package
- Inside of the robot_sim folder run
- Windows: `py -m build`, Ubuntu: `python3 -m build`
- Windows: `py -m pip install .`, Ubuntu: `pip install .`

# Running
Look at the example.py file provided for how to use
- Try running example.py to make sure it works