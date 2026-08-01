
def assert_trees_all_equal_comparator(equality_comparator: _ai.TLeavesEqCmpFn,
                                      error_msg_fn: _ai.TLeavesEqCmpErrorFn,
                                      *trees: ArrayTree) -> None:
  """Checks that all trees are equal as per the custom comparator for leaves.

  Args:
    equality_comparator: A custom function that accepts two leaves and checks
      whether they are equal. Expected to be transitive.
    error_msg_fn: A function accepting two unequal as per
      ``equality_comparator`` leaves and returning an error message.
    *trees: A sequence of (at least 2) trees to check on equality as per
      ``equality_comparator``.

  Raises:
    ValueError: If ``trees`` does not contain at least 2 elements.
    AssertionError: if ``equality_comparator`` returns `False` for any pair of
                    trees from ``trees``.
  """
  if len(trees) < 2:
    raise ValueError(
        "Assertions over only one tree does not make sense. Maybe you wrote "
        "`assert_trees_xxx([a, b])` instead of `assert_trees_xxx(a, b)`, or "
        "forgot the `error_msg_fn` arg to `assert_trees_all_equal_comparator`?")
  assert_trees_all_equal_structs(*trees)

  def tree_error_msg_fn(l_1: _ai.TLeaf, l_2: _ai.TLeaf, path: str, i_1: int,
                        i_2: int):
    msg = error_msg_fn(l_1, l_2)
    if path:
      return f"Trees {i_1} and {i_2} differ in leaves '{path}': {msg}."
    else:
      return f"Trees (arrays) {i_1} and {i_2} differ: {msg}."

  cmp_fn = functools.partial(_ai.assert_leaves_all_eq_comparator,
                             equality_comparator, tree_error_msg_fn)

  # Trees are guaranteed to have the same structure.
  paths = [
      _ai.convert_jax_path_to_dm_path(path)
      for path, _ in jax.tree_util.tree_flatten_with_path(trees[0])[0]]
  trees_leaves = [jax.tree_util.tree_leaves(tree) for tree in trees]
  for leaf_i, path in enumerate(paths):
    cmp_fn(path, *[leaves[leaf_i] for leaves in trees_leaves])

