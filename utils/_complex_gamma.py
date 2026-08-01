
def _complex_gamma(z: Array) -> Array:
  """Gamma function for complex arguments via exp(loggamma(z))."""
  is_nan = jnp.isnan(z)
  is_pole = (jnp.imag(z) == 0) & (jnp.real(z) == jnp.floor(jnp.real(z))) & (jnp.real(z) <= 0)
  nan_val = jnp.array(complex(jnp.nan, jnp.nan), dtype=z.dtype)
  # Mask poles/NaN to a safe value before calling loggamma, so the
  # unselected path doesn't produce NaN that contaminates gradients
  # via jnp.where's VJP (0 * NaN = NaN).
  safe = is_pole | is_nan
  z_safe = jnp.where(safe, jnp.ones_like(z), z)
  return jnp.where(safe, nan_val, jnp.exp(_complex_loggamma(z_safe)))

