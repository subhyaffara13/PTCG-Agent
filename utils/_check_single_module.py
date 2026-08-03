import subprocess
import sys

def _check_single_module(module):
    pid = subprocess.Popen([sys.executable, '-X', 'faulthandler', '-c',
                            f'import {module}'])
    assert pid.wait() == 0, f'Failed to import {module}'

