from typing import Any

def _attr_repr(value: Any):
  if callable(value) and (
    (isinstance(value, nn.Module) and value.__dict__.get('__name__', None))
    or (not isinstance(value, nn.Module) and getattr(value, '__name__', None))
  ):
    value_rep = value.__name__
  else:
    value_rep = repr(value)
  return value_rep

