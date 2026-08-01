
def in_q(compute_dtype, q_dtype, inp, scale, amax_history):
  new_scale, _ = update_fp8_meta(inp, q_dtype, scale, amax_history)
  qin = quantize(inp, q_dtype, _fm32_to_float32(new_scale), compute_dtype)
  return qin, new_scale

