
def treedef_tuple(treedefs: Iterable[PyTreeDef]) -> PyTreeDef:
  """Makes a tuple treedef from an iterable of child treedefs.

  Args:
    treedefs: iterable of PyTree structures

  Returns:
    a single treedef representing a tuple of the structures

  Examples:
    >>> import jax
    >>> x = [1, 2, 3]
    >>> y = {'a': 4, 'b': 5}
    >>> x_tree = jax.tree.structure(x)
    >>> y_tree = jax.tree.structure(y)
    >>> xy_tree = jax.tree_util.treedef_tuple([x_tree, y_tree])
    >>> xy_tree == jax.tree.structure((x, y))
    True

  See Also:
    - :func:`jax.tree_util.treedef_children`
  """
  return pytree.treedef_tuple(default_registry, list(treedefs))

