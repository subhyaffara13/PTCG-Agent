from typing import Any

def concrete_or_error(force: Any, val: Any, context=""):
  """Like force(val), but gives the context in the error message."""
  if force is None:
    force = lambda x: x
  if isinstance(val, Tracer):
    maybe_concrete = val.to_concrete_value()
    if maybe_concrete is None:
      raise ConcretizationTypeError(val, context)
    else:
      return force(maybe_concrete)
  else:
    return force(val)

