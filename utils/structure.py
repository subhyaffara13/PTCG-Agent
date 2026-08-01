
def structure(tree: Any,
              is_leaf: None | (Callable[[Any], bool]) = None) -> tree_util.PyTreeDef:
  """Gets the treedef for a pytree.

  Args:
    tree: the pytree for which to get the leaves
    is_leaf : an optionally specified function that will be called at each
      flattening step. It should return a boolean, which indicates whether the
      flattening should traverse the current object, or if it should be stopped
      immediately, with the whole subtree being treated as a leaf.

  Returns:
    pytreedef: a PyTreeDef representing the structure of the tree.

  Examples:
    >>> import jax
    >>> jax.tree.structure([1, (2, 3), [4, 5]])
    PyTreeDef([*, (*, *), [*, *]])

  See Also:
    - :func:`jax.tree.flatten`
    - :func:`jax.tree.leaves`
    - :func:`jax.tree.unflatten`
  """
  return tree_util.tree_structure(tree, is_leaf)

