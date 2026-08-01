
def add_repr(cls: _ClsT) -> _ClsT:
  """Add a `.__repr__` method to the class, if not already present."""
  # Use `cls.__dict__` and not `hasattr` to ignore parent classes
  if '__repr__' not in cls.__dict__:
    return cls
  if epy.text_utils.has_default_repr(cls):
    cls.__repr__ = __repr__
  return cls

