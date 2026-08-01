
def _fold_and_get_constant_value(x):
  try:
    return _fold(x, 10)
  except FoldingError:
    return None

