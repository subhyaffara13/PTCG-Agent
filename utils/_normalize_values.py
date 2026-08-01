
def _normalize_values(x):
  if isinstance(x, type):
    return f'type[{x.__name__}]'
  elif isinstance(x, ArrayRepr | SimpleObjectRepr):
    return str(x)
  else:
    return repr(x)

