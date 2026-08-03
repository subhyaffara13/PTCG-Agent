from typing import Any

def tree_add(tree_x: Any, tree_y: Any, *other_trees: Any) -> Any:
  r"""Add two (or more) pytrees.

  Args:
    tree_x: first pytree.
    tree_y: second pytree.
    *other_trees: optional other trees to add

  Returns:
    the sum of the two (or more) pytrees.

  .. versionchanged:: 0.2.1
    Added optional ``*other_trees`` argument.
  """
  trees = [tree_x, tree_y, *other_trees]
  return jax.tree.map(lambda *leaves: sum(leaves), *trees)

