import os

def _open_setup_script(setup_script):
    if not os.path.exists(setup_script):
        # Supply a default setup.py
        return io.StringIO("from setuptools import setup; setup()")

    return tokenize.open(setup_script)

