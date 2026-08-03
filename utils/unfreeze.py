from typing import Any

def unfreeze(x: FrozenDict | dict[str, Any]) -> dict[Any, Any]:
  """Unfreeze a FrozenDict.

  Makes a mutable copy of a ``FrozenDict`` mutable by transforming
  it into (nested) dict.

  Args:
    x: Frozen dictionary to unfreeze.
  Returns:
    The unfrozen dictionary (a regular Python dict).
  """
  if isinstance(x, FrozenDict):
    # deep copy internal state of a FrozenDict
    # the dict branch would also work here but
    # it is much less performant because jax.tree_util.tree_map
    # uses an optimized C implementation.
    return jax.tree_util.tree_map(lambda y: y, x._dict)  # type: ignore
  elif isinstance(x, dict):
    ys = {}
    for key, value in x.items():
      ys[key] = unfreeze(value)
    return ys
  else:
    return x

