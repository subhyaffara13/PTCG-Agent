
def _aol_ns_iterator(i, x, coeffs):
  # Modified first step using AOL rescaling
  return jax.lax.cond(
      i == 0,
      lambda x: _aol_first_newton_schulz_iteration(x, coeffs),
      lambda x: _base_newton_schulz_iteration(x, coeffs),
      x,
  )

