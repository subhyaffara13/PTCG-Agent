import sys

def is_gil_disabled() -> bool:
  return not sys._is_gil_enabled() if hasattr(sys, "_is_gil_enabled") else False

