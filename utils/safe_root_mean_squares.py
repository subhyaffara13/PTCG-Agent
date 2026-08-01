
def safe_root_mean_squares(
    x: jax.typing.ArrayLike, min_rms: jax.typing.ArrayLike) -> jax.Array:
  """Returns `maximum(sqrt(mean(abs_sq(x))), min_norm)` with correct grads.

  The gradients of `maximum(sqrt(mean(abs_sq(x))), min_norm)` at 0.0
  is `NaN`, because jax will evaluate both branches of the `jnp.maximum`. This
  function will instead return the correct gradient of 0.0 also in such setting.

  Args:
    x: jax array.
    min_rms: lower bound for the returned norm.

  Returns:
    The safe RMS of the input vector, accounting for correct gradient.
  """
  rms = jnp.sqrt(jnp.mean(abs_sq(x)))
  x = jnp.where(rms <= min_rms, jnp.ones_like(x), x)
  return jnp.where(rms <= min_rms, min_rms, jnp.sqrt(jnp.mean(abs_sq(x))))

