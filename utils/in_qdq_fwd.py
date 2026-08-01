
def in_qdq_fwd(compute_dtype, q_dtype, inp, scale, amax_history):
  qin, new_scale, new_history = quantize_dequantize_update(
    inp, q_dtype, scale, amax_history, compute_dtype
  )
  return qin, (new_scale, new_history)

