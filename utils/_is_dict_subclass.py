
def _is_dict_subclass(obj: Any, *, force: bool = False) -> bool:
  """Returns `True` if the object is a dict subclass."""
  if not isinstance(obj, dict):
    return False
  if force:  # Force pretty-print even if custom `__repr__`
    return True
  if type(obj).__repr__ in (  # Default repr
      dict.__repr__,
      collections.OrderedDict.__repr__,
  ):
    return True
  return False  # Custom repr, do not pretty-print

