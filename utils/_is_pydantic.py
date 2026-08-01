
def _is_pydantic(obj: Any, *, force: bool = False) -> bool:
  """Returns `True` if the object is a `pydantic` dataclass."""
  if 'pydantic' not in sys.modules:
    return False

  import pydantic  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  if not isinstance(obj, pydantic.BaseModel):
    return False
  if force:  # Force pretty-print even if custom `__repr__`
    return True
  if type(obj).__repr__ == pydantic.BaseModel.__repr__:  # Default repr
    return True
  return False  # Custom repr, do not pretty-print

