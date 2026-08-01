
def _bcoo_dot_general_sampled_slow(A, B, indices, *, dimension_numbers, precision):
  return _bcoo_extract(indices, lax.dot_general(A, B, dimension_numbers=dimension_numbers, precision=precision))

