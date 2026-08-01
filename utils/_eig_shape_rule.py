
def _eig_shape_rule(
    shape, *, compute_left_eigenvectors, compute_right_eigenvectors, **_
):
  if shape[0] != shape[1]:
    raise ValueError(
        f"The input to eig must be a square matrix. Got shape {shape}.")
  count = compute_left_eigenvectors + compute_right_eigenvectors
  return (shape[:-1],) + (shape,) * count

