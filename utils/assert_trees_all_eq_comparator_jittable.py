
def assert_trees_all_eq_comparator_jittable(
    equality_comparator: TLeavesEqCmpFn,
    error_msg_template: str,
    *trees: Sequence[pytypes.ArrayTree]) -> pytypes.Array:
  """Asserts all trees are equal using custom comparator. JIT-friendly."""

  if len(trees) < 2:
    raise ValueError(
        "Assertions over only one tree does not make sense. Maybe you wrote "
        "`assert_trees_xxx([a, b])` instead of `assert_trees_xxx(a, b)`, or "
        "forgot the `error_msg_fn` arg to `assert_trees_xxx`?")

  def _tree_error_msg_fn(
      path: Tuple[Union[int, str, Hashable]], i_1: int, i_2: int):
    if path:
      return (
          f"Trees {i_1} and {i_2} differ in leaves '{path}':"
          f" {error_msg_template}"
      )
    else:
      return f"Trees (arrays) {i_1} and {i_2} differ: {error_msg_template}."

  def _cmp_leaves(path, *leaves):
    verdict = jnp.array(True)
    for i in range(1, len(leaves)):
      check_res = equality_comparator(leaves[0], leaves[i])
      checkify.check(
          pred=check_res,
          msg=_tree_error_msg_fn(path, 0, i),
          arr_1=leaves[0],
          arr_2=leaves[i],
      )
      verdict = jnp.logical_and(verdict, check_res)
    return verdict

  # Trees are guaranteed to have the same structure.
  paths = [
      convert_jax_path_to_dm_path(path)
      for path, _ in jax.tree_util.tree_flatten_with_path(trees[0])[0]]
  trees_leaves = [jax.tree_util.tree_leaves(tree) for tree in trees]

  verdict = jnp.array(True)
  for leaf_i, path in enumerate(paths):
    verdict = jnp.logical_and(
        verdict, _cmp_leaves(path, *[leaves[leaf_i] for leaves in trees_leaves])
    )

  return verdict

