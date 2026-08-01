
def _cholesky_shape_rule(shape):
  if shape[0] != shape[1]:
    raise ValueError(
        f"The input to cholesky must be a square matrix. Got shape {shape}.")
  return shape

