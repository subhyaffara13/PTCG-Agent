
def poly_div(a, b):
  """Polynomial division: floor(a / b)."""
  q = 0
  while a.bit_length() >= b.bit_length():
    q ^= 1 << (a.bit_length() - b.bit_length())
    a ^= b << (a.bit_length() - b.bit_length())
  return q

