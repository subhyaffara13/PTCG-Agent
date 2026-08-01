
def quantized_dot(
    lhs,
    q_lhs,
    lhs_scale,  # scale for this step
    rhs,
    q_rhs,
    rhs_scale,  # scale for this step
    out_grad_scale, # scale from previous step
    out_grad_amax_history, # amax history from previous step
    dimension_numbers,
    preferred_element_type=None
):
  return lax.dot_general(
      q_lhs,
      q_rhs,
      dimension_numbers,
      preferred_element_type=preferred_element_type,
      precision=lax.Precision.DEFAULT,
  )

