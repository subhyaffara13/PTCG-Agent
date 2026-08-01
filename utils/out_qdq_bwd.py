
def out_qdq_bwd(compute_dtype, q_dtype, res, g):
  scale, amax_history = res
  q_g, new_scale, new_history = quantize_dequantize_update(
    g, q_dtype, scale, amax_history, compute_dtype
  )
  return q_g, new_scale, new_history

