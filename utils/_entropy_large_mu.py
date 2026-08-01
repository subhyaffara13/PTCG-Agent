
def _entropy_large_mu(mu: Array) -> Array:
  """Entropy for large mu (>= 100): Asymptotic approximation.

  Formula: H(λ) ≈ 0.5*log(2πeλ) - 1/(12λ) + O(λ^-2)
  """
  return 0.5 * jnp.log(2 * np.pi * np.e * mu) - 1.0 / (12 * mu)

