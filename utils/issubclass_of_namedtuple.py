
def issubclass_of_namedtuple(t: Any) -> bool:
  """Determines if the `type` is a subclass of NamedTuple."""
  return issubclass(t, tuple) and hasattr(t, '_fields')

