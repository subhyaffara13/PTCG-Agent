
def _gaussian_kernel_convolve(chol, norm, target, weights, mean):
  diff = target - mean[:, None]
  alpha = linalg.cho_solve(chol, diff)
  arg = 0.5 * jnp.sum(diff * alpha, axis=0)
  return norm * jnp.sum(jnp.exp(-arg) * weights)

