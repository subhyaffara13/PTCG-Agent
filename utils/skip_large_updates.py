
def skip_large_updates(
    updates: base.Updates,
    gradient_step: jax.typing.ArrayLike,
    params: Optional[base.Params],
    max_squared_norm: jax.typing.ArrayLike,
) -> tuple[jax.Array, base.ArrayTree]:
  """Returns True if the global norm square of `updates` is small enough.

  Args:
    updates: see :py:class:`.ShouldSkipUpdateFunction`.
    gradient_step: see :py:class:`.ShouldSkipUpdateFunction`.
    params: see :py:class:`.ShouldSkipUpdateFunction`.
    max_squared_norm: max square norm that can be accepted in updates.

  Returns:
    A tuple:
    * First element is a scalar array of type bool.
    * Second element is a dictionary with keys:
      - `should_skip`: iff ||updates||^2 is greater than `max_squared_norm`.
      - `norm_squared`: overall norm square of the `updates`.
  """
  del gradient_step, params
  norm_sq = jnp.sum(
      jnp.array([jnp.sum(p**2) for p in jax.tree.leaves(updates)])
  )
  # This will also return True if `norm_sq` is NaN.
  should_skip = jnp.logical_not(norm_sq < max_squared_norm)
  return should_skip, {'should_skip': should_skip, 'norm_squared': norm_sq}

