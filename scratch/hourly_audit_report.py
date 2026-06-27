import logging
import subprocess

logger = logging.getLogger(__name__)


def run_cmd(cmd):
    print(f"Executing: {cmd}")
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.stdout:
            print(res.stdout[-800:])
        if res.stderr:
            print(res.stderr[-800:])
    except Exception as e:
        logger.error("Command failed: %s", e)
