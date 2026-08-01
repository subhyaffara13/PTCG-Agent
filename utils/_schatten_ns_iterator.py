
def _schatten_ns_iterator(i, x, coeffs):
  # Modified first step using Schatten-4 norm rescaling
  return jax.lax.cond(
      i == 0,
      lambda x: _schatten_first_newton_schulz_iteration(x, coeffs),
      lambda x: _base_newton_schulz_iteration(x, coeffs),
      x,
  )

