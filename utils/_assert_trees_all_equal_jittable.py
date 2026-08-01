
def _assert_trees_all_equal_jittable(
    *trees: ArrayTree, strict: bool = True,
) -> Array:
  """A jittable version of `_assert_trees_all_equal_static`."""
  if not strict:
    raise NotImplementedError(
        "`strict=False` is not implemented by"
        " `_assert_trees_all_equal_jittable`. This is a feature of"
        " `np.testing.assert_array_equal` used in the static implementation of"
        " `assert_trees_all_equal` that we do not implement in the jittable"
        " version."
    )

  err_msg_template = "Values not exactly equal: {arr_1} != {arr_2}."
  cmp_fn = lambda x, y: jnp.array_equal(x, y, equal_nan=True)
  return _ai.assert_trees_all_eq_comparator_jittable(
      cmp_fn, err_msg_template, *trees
  )

