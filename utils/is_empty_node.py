
def is_empty_node(x: Any) -> bool:
  try:
    children, _ = jax._src.tree_util.flatten_one_level(x)  # pylint: disable=protected-access
  except ValueError:
    return False  # non-empty leaf, otherwise flatten would return self.
  return not children

