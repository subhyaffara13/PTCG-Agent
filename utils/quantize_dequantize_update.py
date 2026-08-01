
def quantize_dequantize_update(x, q_dtype, scale, amax_history, compute_dtype):
  updated_scale, updated_history = update_fp8_meta(x, q_dtype, scale, amax_history)
  qdq_x = qdq(x, q_dtype, _fm32_to_float32(updated_scale), compute_dtype)
  return qdq_x, updated_scale, updated_history

