
def _entropy_medium_mu(mu: Array) -> Array:
  """Entropy for medium mu (10-100): Adaptive bounds based on std dev.

  Bounds: k ≤ μ + 10√μ + 20. Caps at k=250 for JIT compatibility.
  """
  max_k = 250  # Static bound for JIT. For mu<100, upper bound < 220

  k = jnp.arange(max_k, dtype=mu.dtype)[:, None]
  probs = pmf(k, mu, 0)

  upper_bounds = jnp.ceil(mu + 10 * jnp.sqrt(mu) + 20).astype(k.dtype)
  mask = k < upper_bounds[None, :]
  probs_masked = jnp.where(mask, probs, 0.0)

  return jnp.sum(entr(probs_masked), axis=0)

