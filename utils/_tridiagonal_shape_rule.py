
def _tridiagonal_shape_rule(shape, **_):
  if shape[0] != shape[1] or shape[1] == 0:
    raise ValueError(
        f"The input to tridiagonal must be a square matrix. Got shape {shape}.")
  n, _ = shape
  return shape, (n,), (n - 1,), (n - 1,)

