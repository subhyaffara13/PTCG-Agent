
def _running_under_ipython() -> bool:
  """Returns true if we appear to be in an IPython session."""
  try:
    get_ipython()  # pyrefly: ignore[unknown-name]
    return True
  except NameError:
    return False

