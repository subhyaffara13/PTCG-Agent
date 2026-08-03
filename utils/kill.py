import os
import subprocess
import sys

def kill(pid: int) -> None:
    """Kill the process."""
    if sys.platform == "win32":
        subprocess.check_output(f"taskkill /pid {pid} /f /t")
    else:
        os.kill(pid, signal.SIGKILL)

