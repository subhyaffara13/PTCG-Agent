
def _orthonormalize(basis):
  # Twice is enough, again.
  for _ in range(2):
    basis = _svqb(basis)
  return basis

