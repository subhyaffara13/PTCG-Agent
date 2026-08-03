from typing import Any, Callable

def leaves(tree: Any,
           is_leaf: Callable[[Any], bool] | None = None
           ) -> list[tree_util.Leaf]:
  """Gets the leaves of a pytree.

  Args:
    tree: the pytree for which to get the leaves
    is_leaf : an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    leaves: a list of tree leaves.

  Examples:
    >>> import jax
    >>> jax.tree.leaves([1, (2, 3), [4, 5]])
    [1, 2, 3, 4, 5]

  See Also:
    - :func:`jax.tree.flatten`
    - :func:`jax.tree.structure`
    - :func:`jax.tree.unflatten`
  """
  return tree_util.tree_leaves(tree, is_leaf)

