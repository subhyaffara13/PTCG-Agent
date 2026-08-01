
def _cholesky_update_shape_rule(r_shape, w_shape):
  if r_shape[0] != r_shape[1] or w_shape[0] != r_shape[1]:
    raise ValueError(
        "Rank-1 update to Cholesky decomposition takes a square matrix "
        f"and a vector of the same size as input. Got shapes {r_shape} and "
        f"{w_shape} instead")
  return r_shape

