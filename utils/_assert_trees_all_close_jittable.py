
def _assert_trees_all_close_jittable(
    *trees: ArrayTree,
    rtol: float = 1e-06,
    atol: float = 0.0,
    strict: bool = False,
) -> Array:
  """A jittable version of `_assert_trees_all_close_static`."""
  if strict:
    raise NotImplementedError(
        "`strict=True` is not implemented by"
        " `_assert_trees_all_close_jittable`."
    )

  err_msg_template = (
      f"Values not approximately equal ({rtol=}, {atol=}): "
      + "{arr_1} != {arr_2}."
  )
  cmp_fn = lambda x, y: jnp.isclose(x, y, rtol=rtol, atol=atol).all()
  return _ai.assert_trees_all_eq_comparator_jittable(
      cmp_fn, err_msg_template, *trees
  )

