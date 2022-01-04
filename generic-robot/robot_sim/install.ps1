Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile $PSScriptRoot\get-pip.py
python $PSScriptRoot\get-pip.py
python -m pip install --upgrade build
python -m pip install -U pygame --user

python -m build
python -m pip install .
