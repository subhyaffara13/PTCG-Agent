import sys

def _is_in_app_main() -> bool:
  """Returns True iff app.run is active."""
  f = sys._getframe().f_back  # pylint: disable=protected-access
  while f:
    if f.f_code == app.run.__code__:
      return True
    f = f.f_back
  return False

