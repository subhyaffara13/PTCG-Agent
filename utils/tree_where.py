
def tree_where(condition, tree_x, tree_y):
  """Select tree_x values if condition is true else tree_y values.

  Args:
    condition: boolean specifying which values to select from tree x or tree_y
    tree_x: pytree chosen if condition is True
    tree_y: pytree chosen if condition is False

  Returns:
    tree_x or tree_y depending on condition.
  """
  return jax.tree.map(lambda x, y: jnp.where(condition, x, y), tree_x, tree_y)

