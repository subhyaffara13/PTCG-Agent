
def _svd_computation_attr(compute_uv, full_matrices):
  mode = "A"
  if full_matrices is None:
    full_matrices = True
  if not compute_uv:
    mode = "N"
  elif not full_matrices:
    mode = "S"
  return _char_attr(mode)

