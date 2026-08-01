
def dot_general_with_precision_jvp(
  dimension_numbers, precision, preferred_element_type, primals, tangents
):
  lhs, rhs = primals
  lhs_dot, rhs_dot = tangents

  out = lax.dot_general(
    lhs, rhs, dimension_numbers, precision=lax.Precision.DEFAULT
  )
  grad_out = lax.dot_general(
    lhs_dot, rhs, dimension_numbers, precision=lax.Precision.HIGHEST
  ) + lax.dot_general(
    lhs, rhs_dot, dimension_numbers, precision=lax.Precision.HIGHEST
  )
  return out, grad_out

