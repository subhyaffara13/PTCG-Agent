
def in_q_bwd(compute_dtype, q_dtype, res, _):
  new_scale, new_history = res
  # We don't compute gradients for inp, scale and amax_history, but we pass through scale and history
  return None, new_scale, new_history

