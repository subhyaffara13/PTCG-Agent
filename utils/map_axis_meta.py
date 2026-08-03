from typing import Any, Callable

def map_axis_meta(fn: Callable[[AxisMetadata[Any]], Any], tree: Any) -> Any:
  """Maps over all PyTree nodes that are AxisMetadata instances."""

  def wrapper(x):
    if isinstance(x, AxisMetadata):
      return fn(x)
    else:
      return x

  return jax.tree_util.tree_map(wrapper, tree, is_leaf=is_axis_metadata)

