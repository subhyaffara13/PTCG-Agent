
def poly_mul(a, b):
  """Polynomial multiplication: a * b."""
  product = 0
  for i in range(b.bit_length()):
    if (b & (1 << i)) != 0:
      product ^= a << i
  return product

