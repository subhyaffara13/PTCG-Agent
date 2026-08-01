
def _tridiagonal_solve_shape_rule(dl_shape, d_shape, du_shape, b_shape, **_):
  if dl_shape != d_shape or dl_shape != du_shape:
    raise TypeError(
        "tridiagonal_solve requires that all diagonal arguments have the same "
        "shape.")
  if dl_shape != b_shape[:-1]:
    raise TypeError(
        "tridiagonal_solve requires that the leading ndim-1 dimensions of b "
        "equal the dimensions of the diagonal arguments.")
  return b_shape

