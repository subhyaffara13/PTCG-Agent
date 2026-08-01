
def _integer_pow_jvp(g, x, *, y):
  if y == 0:
    return _zeros(g)
  if y == 1:
    return g
  if y == 2:
    return mul(g, mul(_const(x, y), x))
  return mul(g, mul(_const(x, y), integer_pow(x, y - 1)))

