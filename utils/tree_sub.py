from typing import Any

def tree_sub(tree_x: Any, tree_y: Any) -> Any:
  r"""Subtract two pytrees.

  Args:
    tree_x: first pytree.
    tree_y: second pytree.

  Returns:
    the difference of the two pytrees.
  """
  return jax.tree.map(operator.sub, tree_x, tree_y)

