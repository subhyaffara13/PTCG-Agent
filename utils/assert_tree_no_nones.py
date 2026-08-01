
def assert_tree_no_nones(tree: ArrayTree) -> None:
  """Checks that a tree does not contain `None`.

  Args:
    tree: A tree to assert.

  Raises:
    AssertionError: If the tree contains at least one `None`.
  """
  has_nones = False

  def _is_leaf(value):
    if value is None:
      nonlocal has_nones
      has_nones = True
    return False

  treedef = jax.tree_util.tree_structure(tree, is_leaf=_is_leaf)
  if has_nones:
    raise AssertionError(f"Tree contains `None`(s): {treedef}.")

