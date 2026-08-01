
def fp8_scaled_dot_general(
    lhs,
    rhs,
    dimension_numbers,
    precision=None,
    preferred_element_type=None,
    *,
    lhs_scale=None,
    rhs_scale=None,
    grad_scale=None,
    lhs_amax_history=None,
    rhs_amax_history=None,
    grad_amax_history=None,
    quantize_compute_type=jnp.float32,
):
  if precision != None:
    warnings.warn(
      'The function fp8_scaled_dot_general will set the "precision" and '
      'disregard any provided "precision" argument.'
    )
  q_lhs, new_lhs_scale = in_q(
      quantize_compute_type, jnp.float8_e4m3fn, lhs, lhs_scale, lhs_amax_history
  )
  q_rhs, new_rhs_scale = in_q(
      quantize_compute_type, jnp.float8_e4m3fn, rhs, rhs_scale, rhs_amax_history
  )
  y = quantized_dot(
      lhs,
      q_lhs,
      new_lhs_scale,
      rhs,
      q_rhs,
      new_rhs_scale,
      grad_scale,
      grad_amax_history,
      dimension_numbers,
      preferred_element_type
  )
  y = out_dq(
      dq_type=preferred_element_type,
      lhs_scale=new_lhs_scale,
      rhs_scale=new_rhs_scale,
      out=y
  )
  return y  # type: ignore

