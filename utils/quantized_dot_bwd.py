
def quantized_dot_bwd(
    dimension_numbers,
    preferred_element_type,
    res,
    g
):
  (
      lhs,
      q_lhs,
      lhs_scale,
      rhs,
      q_rhs,
      rhs_scale,
      out_grad_scale,
      out_grad_amax_history,
  ) = res

  new_out_grad_scale, new_out_grad_amax_history = update_fp8_meta(
      g,
      jnp.float8_e5m2,
      out_grad_scale,
      out_grad_amax_history,
  )

  q_g = quantize(
      g,
      jnp.float8_e5m2,
      _fm32_to_float32(new_out_grad_scale),
      preferred_element_type
  )

  grad_lhs = dot_general_transpose_lhs(
      q_g,
      lhs,
      q_rhs,
      dimension_numbers=dimension_numbers,
      precision=lax.Precision.HIGHEST,
      preferred_element_type=preferred_element_type,
  )

  grad_lhs = dequantize(
      grad_lhs,
      preferred_element_type,
      _fm32_to_float32(rhs_scale) * _fm32_to_float32(new_out_grad_scale)
  )

  grad_rhs = dot_general_transpose_rhs(
      q_g,
      q_lhs,
      rhs,
      dimension_numbers=dimension_numbers,
      precision=lax.Precision.HIGHEST,
      preferred_element_type=preferred_element_type,
  )

  grad_rhs = dequantize(
      grad_rhs,
      preferred_element_type,
      _fm32_to_float32(lhs_scale) * _fm32_to_float32(new_out_grad_scale)
  )

  return (
      grad_lhs,
      None,
      None,
      grad_rhs,
      None,
      None,
      new_out_grad_scale,
      new_out_grad_amax_history,
  )

