
def poly_exp(a, b, g):
  """Polynomial exponentiation: a^b mod g."""
  if b == 1:
    return poly_reduce(a, g)
  c = poly_exp(a, b // 2, g)
  c = poly_mul(c, c)
  if b % 2 != 0:
    c = poly_mul(c, a)
  return poly_reduce(c, g)

