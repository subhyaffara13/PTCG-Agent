
def _represent_tree(x):
  """Returns a tree with the same structure as `x` but with each leaf replaced
  by a `_ValueRepresentation` object."""
  return jax.tree_util.tree_map(
    _get_value_representation,
    x,
    is_leaf=lambda x: x is None or isinstance(x, meta.Partitioned),
  )

