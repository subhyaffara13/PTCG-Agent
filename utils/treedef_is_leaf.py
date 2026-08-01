
def treedef_is_leaf(treedef: PyTreeDef) -> bool:
  """Return True if the treedef represents a leaf.

  Args:
    treedef: tree to check

  Returns:
    True if treedef is a leaf (i.e. has a single node); False otherwise.

  Examples:
    >>> import jax
    >>> tree1 = jax.tree.structure(1)
    >>> jax.tree_util.treedef_is_leaf(tree1)
    True
    >>> tree2 = jax.tree.structure([1, 2])
    >>> jax.tree_util.treedef_is_leaf(tree2)
    False
  """
  return treedef.num_nodes == 1

