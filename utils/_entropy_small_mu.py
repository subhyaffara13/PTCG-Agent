
def _entropy_small_mu(mu: Array) -> Array:
  """Entropy via direct PMF summation for small μ (< 10).
  Uses adaptive upper bound k ≤ μ + 20 to capture >99.999% of mass.
  """
  max_k = 35

  k = jnp.arange(max_k, dtype=mu.dtype)[:, None]
  probs = pmf(k, mu, 0)

  # Mask: only compute up to mu + 20 for each value
  upper_bounds = jnp.ceil(mu + 20).astype(k.dtype)
  mask = k < upper_bounds[None, :]
  probs_masked = jnp.where(mask, probs, 0.0)

  return jnp.sum(entr(probs_masked), axis=0)

