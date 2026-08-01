
def _put_variable(target, key, val):
  if (
      key in target
      and isinstance(target[key], dict)
      and isinstance(val, Mapping)
  ):
    for k, v in val.items():
      _put_variable(target[key], k, v)
  else:
    target[key] = val

