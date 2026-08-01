
def unitwise_clip(
    g_norm: jax.typing.ArrayLike,
    max_norm: jax.typing.ArrayLike,
    grad: jax.typing.ArrayLike,
    div_eps: jax.typing.ArrayLike = 1e-6,
) -> jax.Array:
  """Applies gradient clipping unit-wise."""
  # This little max(., div_eps) is distinct from the normal eps and just
  # prevents division by zero. It technically should be impossible to engage.
  clipped_grad = grad * (max_norm / jnp.maximum(g_norm, div_eps))
  utils.check_shapes_equal(g_norm, max_norm)
  utils.check_shapes_equal(g_norm, grad)
  return jnp.where(g_norm < max_norm, grad, clipped_grad)

