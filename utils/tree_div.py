from typing import Any

def tree_div(tree_x: Any, tree_y: Any) -> Any:
  r"""Divide two pytrees.

  Args:
    tree_x: first pytree.
    tree_y: second pytree.

  Returns:
    the quotient of the two pytrees.
  """
  return jax.tree.map(operator.truediv, tree_x, tree_y)

