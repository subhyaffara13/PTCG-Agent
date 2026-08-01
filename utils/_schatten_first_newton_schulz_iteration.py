
def _schatten_first_newton_schulz_iteration(
    x: jax.Array,
    coeffs: jax.Array,
    eps: jax.typing.ArrayLike = 1e-8,
) -> jax.Array:
  """Schatten-4 Preconditioning with Newton-Schulz iteration."""
  # Implements the first Newton-Schulz step with Schatten-4 norm
  # preconditioning which allows for better orthogonalization performance.
  a = x @ x.T
  rescaling = jnp.clip(jnp.linalg.norm(a, ord='fro', axis=(-2, -1)), min=eps)
  s = jnp.expand_dims(jax.lax.rsqrt(rescaling), (0, -1))
  x, a = x * s, a * s ** 2
  b = coeffs[1] * a + coeffs[2] * a @ a
  return coeffs[0] * x + b @ x

