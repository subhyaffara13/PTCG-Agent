
def _eq_meet(a, b):
  a_dtype, b_dtype = _dtype(a), _dtype(b)
  if a_dtype != b_dtype:
    higher_dtype = dtypes.promote_types(a_dtype, b_dtype)
    if higher_dtype == a_dtype:
      a = convert_element_type(a, b_dtype)
    else:
      b = convert_element_type(b, a_dtype)
  return eq(a, b)

