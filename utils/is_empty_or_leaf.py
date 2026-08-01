
def is_empty_or_leaf(x: Any) -> bool:
  try:
    children, _ = jax._src.tree_util.flatten_one_level(x)  # pylint: disable=protected-access
  except ValueError:
    return True  # Cannot flatten x; means it must be a leaf
  return not children

