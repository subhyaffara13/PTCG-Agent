
def _check_compatible_avals(a: core.AbstractValue, b: core.AbstractValue) -> bool:
  if isinstance(a, core.AbstractToken) and isinstance(b, core.AbstractToken):
    return True
  if getattr(a, "shape", ()) != getattr(b, "shape", ()):
    return False
  if getattr(a, "dtype", ()) != getattr(b, "dtype", ()):
    return False
  return True

