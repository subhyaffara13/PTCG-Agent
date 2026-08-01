
def _is_callable_type(field_type):
  """Tries to ensure: `_is_callable_type(type(obj)) == callable(obj)`."""
  return any('__call__' in c.__dict__ for c in field_type.__mro__)

