
def poly_reduce(a, b):
  """Polynomial reduction: a mod b."""
  return a ^ poly_mul(poly_div(a, b), b)

