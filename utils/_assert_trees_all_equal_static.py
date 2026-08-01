
def _assert_trees_all_equal_static(
    *trees: ArrayTree, strict: bool = False
) -> None:
  """Checks that all trees have leaves with *exactly* equal values.

  If you are comparing floating point numbers, an exact equality check may not
  be appropriate; consider using ``assert_trees_all_close``.

  Args:
    *trees: A sequence of (at least 2) trees with array leaves.
    strict: If True, disable special scalar handling as described in
      `np.testing.assert_array_equals` notes section.

  Raises:
    AssertionError: If the leaf values actual and desired are not exactly equal.
  """
  def assert_fn(arr_1, arr_2):
    if isinstance(arr_1, jax.Array) and jax.dtypes.issubdtype(
        arr_1.dtype, jax.dtypes.prng_key
    ) and isinstance(arr_2, jax.Array) and jax.dtypes.issubdtype(
        arr_2.dtype, jax.dtypes.prng_key
    ):
      assert jax.random.key_impl(arr_1) == jax.random.key_impl(arr_2)
      arr_1 = jax.random.key_data(arr_1)
      arr_2 = jax.random.key_data(arr_2)
    np.testing.assert_array_equal(
        _ai.jnp_to_np_array(arr_1),
        _ai.jnp_to_np_array(arr_2),
        err_msg="Error in value equality check: Values not exactly equal",
        strict=strict,
    )

  def cmp_fn(arr_1, arr_2) -> bool:
    try:
      # Raises an AssertionError if values are not equal.
      assert_fn(arr_1, arr_2)
    except AssertionError:
      return False
    return True

  def err_msg_fn(arr_1, arr_2) -> str:
    try:
      assert_fn(arr_1, arr_2)
    except AssertionError as e:
      dtype_1 = (
          arr_1.dtype
          if isinstance(arr_1, jax.Array)
          else np.asarray(arr_1).dtype
      )
      dtype_2 = (
          arr_2.dtype
          if isinstance(arr_2, jax.Array)
          else np.asarray(arr_1).dtype
      )
      return f"{str(e)} \nOriginal dtypes: {dtype_1}, {dtype_2}"
    return ""

  assert_trees_all_equal_comparator(cmp_fn, err_msg_fn, *trees)

