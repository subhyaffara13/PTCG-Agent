
def optimal_step_size(last_step, mean_error_ratio, safety=0.9, ifactor=10.0,
                      dfactor=0.2, order=5.0):
  """Compute optimal Runge-Kutta stepsize."""
  dfactor = jnp.where(mean_error_ratio < 1, 1.0, dfactor)

  factor = jnp.minimum(ifactor,
                      jnp.maximum(mean_error_ratio**(-1.0 / order) * safety, dfactor))
  return jnp.where(mean_error_ratio == 0, last_step * ifactor, last_step * factor)

