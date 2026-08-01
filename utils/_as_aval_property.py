
def _as_aval_property(p: property) -> hjx.aval_property:
  """Wraps a property `p` operate on the aval type."""
  _aval_property = hjx.aval_property(fget=p.fget)
  return _aval_property  # type: ignore[return]

