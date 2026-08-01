
def _maybe_int(x):
  try:
    return int(x)
  except (ValueError, TypeError):
    return x

