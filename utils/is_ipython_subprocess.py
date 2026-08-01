
def is_ipython_subprocess() -> bool:
  """Check if we are in a sub-process launched from within a `ipython` terminal.

  Returns:
    `True` only if we are in ipython terminal (e.g. `ml_python`) and inside
    a sub-process.
  """
  return False

