from typing import Any

def _freeze_attr(val: Any) -> Any:
  """Recursively wrap the given attribute `var` in ``FrozenDict``."""
  if isinstance(val, (dict, FrozenDict)):
    return FrozenDict({k: _freeze_attr(v) for k, v in val.items()})
  elif isinstance(val, tuple):
    # Special case namedtuples and special JAX tuple structures otherwise they
    # would be downgraded to normal tuples.
    if hasattr(val, '_fields') or type(val).__name__ == 'PartitionSpec':
      return type(val)(*[_freeze_attr(v) for v in val])
    else:
      return tuple(_freeze_attr(v) for v in val)
  elif isinstance(val, list):
    return tuple(_freeze_attr(v) for v in val)
  else:
    return val

