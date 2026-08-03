import sys

def is_running_under_pytest():
  return "pytest" in sys.modules

