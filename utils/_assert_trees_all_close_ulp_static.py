
def _assert_trees_all_close_ulp_static(
    *trees: ArrayTree,
    maxulp: int = 1,
) -> None:
  """Checks that tree leaves differ by at most `maxulp` Units in the Last Place.

  This is the Chex version of np.testing.assert_array_max_ulp.

  Assertions on floating point values are tricky because the precision varies
  depending on the value. For example, with float32, the precision at 1 is
  np.spacing(np.float32(1.0)) ≈ 1e-7, but the precision at 5,000,000 is only
  np.spacing(np.float32(5e6)) = 0.5. This makes it hard to predict ahead of time
  what tolerance to use when checking whether two numbers are equal: a
  difference of only a couple of bits can equate to an arbitrarily large
  absolute difference.

  Assertions based on _relative_ differences are one solution to this problem,
  but have the disadvantage that it's hard to choose the tolerance. If you want
  to verify that two calculations produce _exactly_ the same result
  modulo the inherent non-determinism of floating point operations, do you set
  the tolerance to...0.01? 0.001? It's hard to be sure you've set it low enough
  that you won't miss one of your computations being slightly wrong.

  Assertions based on 'units in the last place' (ULP) instead solve this
  problem by letting you specify tolerances in terms of the precision actually
  available at the current scale of your values. The ULP at some value x is
  essentially the spacing between the floating point numbers actually
  representable in the vicinity of x - equivalent to the 'precision' we
  discussed above. above. With a tolerance of, say, `maxulp=5`, you're saying
  that two values are within 5 actually-representable-numbers of each other -
  a strong guarantee that two computations are as close as possible to
  identical, while still allowing reasonable wiggle room for small differences
  due to e.g. different operator orderings.

  Note that this function is not currently supported within JIT contexts.

  Args:
    *trees: A sequence of (at least 2) trees with array leaves.
    maxulp: The maximum number of ULPs by which leaves may differ.

  Raises:
    AssertionError: If actual and desired values are not equal up to
      specified tolerance.
  """
  def assert_fn(arr_1, arr_2):
    # Get the dtype from the original JAX array, not the NumPy-converted one.
    dtype = getattr(arr_1, "dtype", None)

    # Convert JAX arrays to NumPy arrays for comparison.
    np_arr_1 = _ai.jnp_to_np_array(arr_1)
    np_arr_2 = _ai.jnp_to_np_array(arr_2)

    if dtype == jnp.bfloat16:
      ret = _bfloat16_nulp_diff(np_arr_1, np_arr_2)
      if not np.all(ret <= maxulp):
        raise AssertionError(
            f"Arrays are not almost equal up to {maxulp} ULP for bfloat16 "
            f"(max difference is {np.max(ret)} ULP)"
        )
    else:
      # For all other supported float types, use NumPy's implementation.
      np.testing.assert_array_max_ulp(np_arr_1, np_arr_2, maxulp=maxulp)

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
      return (
          f"{str(e)} \nOriginal dtypes: "
          f"{np.asarray(arr_1).dtype}, {np.asarray(arr_2).dtype}"
      )
    return ""

  assert_trees_all_equal_comparator(cmp_fn, err_msg_fn, *trees)

