from typing import Any

def _prepare_freeze(xs: Any) -> Any:
  """Deep copy unfrozen dicts to make the dictionary FrozenDict safe."""
  if isinstance(xs, FrozenDict):
    # we can safely ref share the internal state of a FrozenDict
    # because it is immutable.
    return xs._dict  # pylint: disable=protected-access
  if not isinstance(xs, dict):
    # return a leaf as is.
    return xs
  # recursively copy dictionary to avoid ref sharing
  return {key: _prepare_freeze(val) for key, val in xs.items()}

