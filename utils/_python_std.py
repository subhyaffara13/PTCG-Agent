import sys

def _python_std(stream: str):
    return {"stdout": sys.stdout, "stderr": sys.stderr}[stream]

