import os
import subprocess

def _run_subprocess_ignore_stderr(command):
    """Return subprocess.check_output with the given command and ignores stderr."""
    with open(os.devnull, "w") as devnull:
        output = subprocess.check_output(command, stderr=devnull)
    return output

