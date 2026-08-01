
def _assert_trees_all_close_static(
    *trees: ArrayTree,
    rtol: float = 1e-06,
    atol: float = 0.0,
    strict: bool = False,
) -> None:
  """Checks that all trees have leaves with approximately equal values.

  This compares the difference between values of actual and desired up to
   ``atol + rtol * abs(desired)``.

  Args:
    *trees: A sequence of (at least 2) trees with array leaves.
    rtol: A relative tolerance.
    atol: An absolute tolerance.
    strict: If True, raise an AssertionError when either the shape or the data
      type of the arguments does not match. The special handling for scalars
      mentioned in the Notes section of `np.allclose` is disabled.

  Raises:
    AssertionError: If actual and desired values are not equal up to
      specified tolerance.
  """
  def assert_fn(arr_1, arr_2):
    np.testing.assert_allclose(
        _ai.jnp_to_np_array(arr_1),
        _ai.jnp_to_np_array(arr_2),
        rtol=rtol,
        atol=atol,
        err_msg="Error in value equality check: Values not approximately equal",
        strict=strict,
    )

  def cmp_fn(arr_1, arr_2) -> bool:
    try:
      # Raises an AssertionError if values are not close.
      assert_fn(arr_1, arr_2)
    except AssertionError:
      return False
    return True

  def err_msg_fn(arr_1, arr_2) -> str:
    try:
      assert_fn(arr_1, arr_2)
    except AssertionError as e:
      return (f"{str(e)} \nOriginal dtypes: "
              f"{np.asarray(arr_1).dtype}, {np.asarray(arr_2).dtype}")
    return ""

  assert_trees_all_equal_comparator(cmp_fn, err_msg_fn, *trees)

