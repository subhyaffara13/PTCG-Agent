
def assert_trees_all_equal_shapes_and_dtypes(*trees: ArrayTree) -> None:
  """Checks that trees' leaves have the same shape and dtype.

  Args:
    *trees: A sequence of (at least 2) trees to check.

  Raises:
    AssertionError: If leaves' shapes or dtypes for any two trees differ.
  """
  assert_trees_all_equal_shapes(*trees)
  assert_trees_all_equal_dtypes(*trees)

