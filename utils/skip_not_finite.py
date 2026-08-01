
def skip_not_finite(
    updates: base.Updates,
    gradient_step: jax.typing.ArrayLike,
    params: Optional[base.Params],
) -> tuple[jax.Array, base.ArrayTree]:
  """Returns True iff any of the `updates` contains an inf or a NaN.

  Args:
    updates: see `ShouldSkipUpdateFunction`.
    gradient_step: see `ShouldSkipUpdateFunction`.
    params: see `ShouldSkipUpdateFunction`.

  Returns:
    A tuple:
    * First element is a scalar array of type bool.
    * Second element is a dictionary with keys:
      - `should_skip`: True iff `updates` contains an inf or a NaN.
      - `num_not_finite`: total number of inf and NaN found in `updates`.
  """
  del gradient_step, params
  all_is_finite = [
      jnp.sum(jnp.logical_not(jnp.isfinite(p)))
      for p in jax.tree.leaves(updates)
  ]
  num_not_finite = jnp.sum(jnp.array(all_is_finite))
  should_skip = num_not_finite > 0
  return should_skip, {
      'should_skip': should_skip,
      'num_not_finite': num_not_finite,
  }

