
def _aol_first_newton_schulz_iteration(
    x: jax.Array,
    coeffs: jax.Array,
    eps: jax.typing.ArrayLike = 1e-8,
) -> jax.Array:
  """'Almost Orthogonal Layer' Preconditioning with Newton-Schulz iteration."""
  # Implements the first Newton-Schulz step with AOL preconditioning
  # which allows for better orthogonalization performance.
  a = x @ x.T.conj()
  rescaling = jnp.clip(jnp.abs(a).sum(axis=-1), min=eps)
  s = jnp.expand_dims(jax.lax.rsqrt(rescaling), -1)
  x, a = x * s, a * s * s.transpose(-1, -2)
  b = coeffs[1] * a + coeffs[2] * a @ a
  return coeffs[0] * x + b @ x

