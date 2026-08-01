
def _pattern_match_lanes_to_sublanes_reshape(
    aval_in: core.ShapedArray,
    aval_out: core.ShapedArray,
) -> bool:
  # Pattern matches a reshape of the form (..., n * l) -> (..., n, l)
  # where l is a multiple of 128.

  *leading_out, last_dim_in = aval_in.shape
  *leading_in, second_to_last_dim_out, last_dim = aval_out.shape
  if leading_in != leading_out:
    return False
  if second_to_last_dim_out * last_dim != last_dim_in:
    return False
  if last_dim % 128 != 0:
    return False
  return True

