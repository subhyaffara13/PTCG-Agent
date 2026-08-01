
def _is_fiddle(obj: Any) -> bool:
  """Returns `True` if the object is a `fiddle` config object."""
  if 'fiddle' not in sys.modules:
    return False
  import fiddle  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error

  return isinstance(obj, fiddle.Config)

