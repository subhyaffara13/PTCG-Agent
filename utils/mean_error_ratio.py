
def mean_error_ratio(error_estimate, rtol, atol, y0, y1):
  err_tol = atol + rtol * jnp.maximum(jnp.abs(y0), jnp.abs(y1))
  err_ratio = error_estimate / err_tol.astype(error_estimate.dtype)
  return jnp.sqrt(jnp.mean(abs2(err_ratio)))

