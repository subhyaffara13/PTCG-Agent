
def dot_general_with_precision(
  lhs, rhs, dimension_numbers, precision=None, preferred_element_type=None
):
  if precision != None or preferred_element_type != None:
    warnings.warn(
      'The function dot_general_with_precision will set the '
      'precision/preferred_element_type and disregard any provided '
      'values.'
    )
  return lax.dot_general(
    lhs, rhs, dimension_numbers, precision=lax.Precision.DEFAULT
  )

