
def _triangular_solve_shape_rule(a_shape, b_shape, *, left_side=False, **_):
  if a_shape[0] != a_shape[1]:
    raise ValueError(
        "The first input to triangular_solve must be a square matrix. Got "
        f"shape {a_shape}.")
  common_dim = -2 if left_side else -1
  if a_shape[-1] != b_shape[common_dim]:
    raise ValueError(
        f"Incompatible shapes for arguments to triangular_solve: {a_shape} and "
        f"{b_shape}.")
  return b_shape

