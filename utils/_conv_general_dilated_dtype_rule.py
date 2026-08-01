
def _conv_general_dilated_dtype_rule(
    lhs, rhs, *, window_strides, padding, lhs_dilation, rhs_dilation,
    dimension_numbers, preferred_element_type, **unused_kwargs):
  result_dtype = lax.naryop_dtype_rule(lax.input_dtype, [lax._any, lax._any],
                                       'conv_general_dilated', lhs, rhs)
  if preferred_element_type is None:
    return result_dtype
  lax._validate_preferred_element_type(result_dtype, preferred_element_type)
  return preferred_element_type

