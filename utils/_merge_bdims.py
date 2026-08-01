
def _merge_bdims(x, y):
  if x == y:
    return x
  elif x is None:
    return y
  elif y is None:
    return x
  else:
    return x  # arbitrary

