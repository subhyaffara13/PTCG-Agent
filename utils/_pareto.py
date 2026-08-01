
def _pareto(key, b, shape, dtype) -> Array:
  b = lax.convert_element_type(b, dtype)
  e = exponential(key, shape, dtype)
  return lax.exp(e / b)

