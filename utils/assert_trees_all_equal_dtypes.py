
def assert_trees_all_equal_dtypes(actual, desired, err_msg=None):
  """Asserts that two pytrees of arrays have the same dtypes."""
  assert_trees_all_equal_structs(actual, desired)
  for x, y in zip(jax.tree_util.tree_leaves(actual),
                  jax.tree_util.tree_leaves(desired)):
    if x.dtype != y.dtype:
      raise AssertionError(
          f"Dtypes are not equal: {x.dtype} != {y.dtype}. {err_msg}"
      )


def assert_trees_all_equal_dtypes(*trees: ArrayTree) -> None:
  """Checks that trees' leaves have the same dtype.

  Args:
    *trees: A sequence of (at least 2) trees to check.

  Raises:
    AssertionError: If leaves' dtypes for any two trees differ.
  """
  def cmp_fn(arr_1, arr_2):
    return (hasattr(arr_1, "dtype") and hasattr(arr_2, "dtype") and
            arr_1.dtype == arr_2.dtype)

  def err_msg_fn(arr_1, arr_2):
    if not hasattr(arr_1, "dtype"):
      return f"{type(arr_1)} is not a (j-)np array (has no `dtype` property)"
    if not hasattr(arr_2, "dtype"):
      return f"{type(arr_2)} is not a (j-)np array (has no `dtype` property)"
    return f"types: {arr_1.dtype} != {arr_2.dtype}"

  assert_trees_all_equal_comparator(cmp_fn, err_msg_fn, *trees)

