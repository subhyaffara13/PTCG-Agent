
def _assert_trees_all_close_ulp_jittable(
    *trees: ArrayTree,
    maxulp: int = 1,
) -> jax.Array:
  """A dummy jittable version of `_assert_trees_all_close_ulp_static`.

  JAX does not yet have a native version of assert_array_max_ulp, so at the
  moment making ULP assertions on tracer objects simply isn't supported.
  This function exists only to make sure a sensible error is given.

  Args:
    *trees: Ignored.
    maxulp: Ignored.

  Raises:
    NotImplementedError: unconditionally.

  Returns:
    Never returns. (We pretend jax.Array to satisfy the type checker.)
  """
  del trees, maxulp
  raise NotImplementedError(
      f"{_ai.ERR_PREFIX}assert_trees_all_close_ulp is not supported within JIT "
      "contexts."
  )

