
def tree_mul(tree_x: Any, tree_y: Any) -> Any:
  r"""Multiply two pytrees.

  Args:
    tree_x: first pytree.
    tree_y: second pytree.

  Returns:
    the product of the two pytrees.
  """
  return jax.tree.map(operator.mul, tree_x, tree_y)

