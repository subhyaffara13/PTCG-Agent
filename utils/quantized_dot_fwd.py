
def quantized_dot_fwd(
    lhs,
    q_lhs,
    lhs_scale,
    rhs,
    q_rhs,
    rhs_scale,
    out_grad_scale,
    out_grad_amax_history,
    dimension_numbers,
    preferred_element_type,
):
  out = lax.dot_general(
      q_lhs,
      q_rhs,
      dimension_numbers,
      preferred_element_type=preferred_element_type,
      precision=lax.Precision.DEFAULT,
  )
  res = (
      lhs,
      q_lhs,
      lhs_scale,
      rhs,
      q_rhs,
      rhs_scale,
      out_grad_scale,
      out_grad_amax_history,
  )
  return out, res

