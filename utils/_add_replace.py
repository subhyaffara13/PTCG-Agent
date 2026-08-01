
def _add_replace(cls: _ClsT) -> _ClsT:
  """Add a `.replace` method to the class, if not already present."""
  # Only add replace if not present
  if not hasattr(cls, 'replace'):
    cls.replace = replace
  return cls

