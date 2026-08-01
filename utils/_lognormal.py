
def _lognormal(key, sigma, shape, dtype) -> Array:
  sigma = lax.convert_element_type(sigma, dtype)
  scaled_norm = normal(key, shape, dtype) * sigma
  return lax.exp(scaled_norm)

