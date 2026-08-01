
def out_dq(dq_type, lhs_scale, rhs_scale, out):
  q_out = dequantize(
    out,
    dq_type,
    _fm32_to_float32(lhs_scale) * _fm32_to_float32(rhs_scale)
  )
  return q_out

