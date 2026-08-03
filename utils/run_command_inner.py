import subprocess
import sys

def run_command_inner(*cmd, **kwargs):
    opts = {
        "stderr": subprocess.STDOUT,
        "stdout": subprocess.PIPE,
        "text": True,
        "encoding": "utf-8",
        "check": True,
        **kwargs,
    }
    cmd = [sys.executable, "-c", "__import__('setuptools').setup()", *map(str, cmd)]
    return subprocess.run(cmd, **opts)

