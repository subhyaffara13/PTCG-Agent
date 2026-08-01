
def _softmax_deprecated(
    x: ArrayLike,
    axis: Axis = -1,
    where: ArrayLike | None = None,
    initial: ArrayLike = -np.inf) -> Array:
  x_max = jnp.max(x, axis, where=where, initial=initial, keepdims=True)
  x_safe = x if where is None else jnp.where(where, x, initial)
  unnormalized = jnp.exp(x_safe - lax.stop_gradient(x_max))
  result = unnormalized / jnp.sum(unnormalized, axis, where=where, keepdims=True)
  if where is not None:
    result = jnp.where(where, result, 0)
  return result

