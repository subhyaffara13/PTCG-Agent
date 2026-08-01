
def _schur_shape_rule(shape, *, compute_schur_vectors, **_):
  if shape[0] != shape[1]:
    raise ValueError(
        f"The input to schur must be a square matrix. Got shape {shape}.")
  return (shape, shape) if compute_schur_vectors else (shape,)

