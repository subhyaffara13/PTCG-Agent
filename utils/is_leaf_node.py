
def is_leaf_node(t: Any) -> bool:
  """The default value of the `is_leaf` predicate."""
  return jax.tree_util.all_leaves([t])

