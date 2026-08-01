
def is_weakly_typed(x: Any) -> bool:
  if type(x) in _weak_types or type(x) in _registered_weak_types:
    return True
  try:
    return x.aval.weak_type
  except AttributeError:
    return False

