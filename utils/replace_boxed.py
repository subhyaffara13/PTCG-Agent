from typing import Any

def replace_boxed(tree: Any, updates: Any) -> Any:
  """Updates all AxisMetadata boxes with the values in updates."""

  def inner_update(c, v):
    if isinstance(c, AxisMetadata):
      return c.replace_boxed(replace_boxed(c.unbox(), v))
    else:
      return v

  return jax.tree_util.tree_map(
      inner_update, tree, updates, is_leaf=is_axis_metadata
  )

