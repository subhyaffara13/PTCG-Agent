
def _IsIterable(obj):
  try:
    iter(obj)
    return True
  except TypeError:
    return False

