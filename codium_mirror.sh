#!/usr/bin/bash

_args=("$@") # All parameters from terminal.

p8(){
    isort setup.py
    autopep8 -i -a -a -r -v setup.py
    isort codium_mirror/__init__.py
    autopep8 -i -a -a -r -v codium_mirror/__init__.py
}


twine_upload(){
    twine upload --verbose dist/*
}

bdist(){
    rm -rf dist/ build/ codium_mirror.egg-info/
    python3 setup.py sdist bdist_wheel
}

_i_test(){
    bdist
    pip3 uninstall codium_mirror -y
    pip3 install dist/*.whl
    codium_mirror
}

tu(){       twine_upload;       }
its(){       _i_test;           }
bdup(){     bdist; tu;          }

${_args[0]}
