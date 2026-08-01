
def treedef_children(treedef: PyTreeDef) -> list[PyTreeDef]:
  """Return a list of treedefs for immediate children

  Args:
    treedef: a single PyTreeDef

  Returns:
    a list of PyTreeDefs representing the children of treedef.

  Examples:
    >>> import jax
    >>> x = [(1, 2), 3, {'a': 4}]
    >>> treedef = jax.tree.structure(x)
    >>> jax.tree_util.treedef_children(treedef)
    [PyTreeDef((*, *)), PyTreeDef(*), PyTreeDef({'a': *})]
    >>> _ == [jax.tree.structure(vals) for vals in x]
    True

  See Also:
    - :func:`jax.tree_util.treedef_tuple`
  """
  return treedef.children()

