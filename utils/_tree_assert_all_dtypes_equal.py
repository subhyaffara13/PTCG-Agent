
def _tree_assert_all_dtypes_equal(
    tree: base.ArrayTree, dtype: jax.typing.DTypeLike
) -> None:
  """Checks that all leaves of the tree have the given dtype.

  Args:
    tree: the tree to check.
    dtype: the dtype to check against.

  Raises:
    ValueError: If any element of the tree does not match the given dtype.
  """

  def _assert_dtypes_equal(path, x):
    x_dtype = jnp.asarray(x).dtype
    if x_dtype != dtype:
      err_msg = f'Expected {dtype=} for {path} but got {x_dtype}.'
      return err_msg
    return None

  err_msgs = jax.tree.leaves(
      jax.tree_util.tree_map_with_path(_assert_dtypes_equal, tree)
  )
  err_msgs = [err_msg for err_msg in err_msgs if err_msg is not None]
  if err_msgs:
    raise ValueError('\n'.join(err_msgs))

