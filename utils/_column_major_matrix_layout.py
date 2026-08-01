
def _column_major_matrix_layout(dim: int) -> tuple[int, ...]:
  # The layout for a batch of matrices with Fortran order.
  return (dim - 2, dim - 1) + tuple(range(dim - 3, -1, -1))

