
def in_qdq_bwd(compute_dtype, q_dtype, res, g):
  new_scale, new_history = res
  q_g = g
  return q_g, new_scale, new_history

