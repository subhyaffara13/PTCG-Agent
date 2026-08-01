
def evaluate_chebyshev_polynomial(x, coefficients):
  b0 = full_like(x,0)
  b1 = full_like(x,0)
  b2 = full_like(x,0)
  for c in coefficients:
    b2 = b1
    b1 = b0
    b0 = x * b1 - b2 + full_like(x, c)
  return 0.5 * (b0 - b2)

