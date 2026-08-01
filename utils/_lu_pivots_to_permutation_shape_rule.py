
def _lu_pivots_to_permutation_shape_rule(shape, *, permutation_size):
  pivots_size, = shape
  if not permutation_size >= pivots_size:
    raise ValueError(
        f"Output permutation size {permutation_size} has to exceed the "
        f"trailing dimension of the pivots. Got pivots size {pivots_size}")
  return (permutation_size,)

