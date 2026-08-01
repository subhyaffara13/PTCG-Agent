
def in_qdq(compute_dtype, q_dtype, inp, scale, amax_history):
  qin, _, _ = quantize_dequantize_update(
    inp, q_dtype, scale, amax_history, compute_dtype
  )
  return qin

