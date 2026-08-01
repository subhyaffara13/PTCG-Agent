
def scaled_dot_fwd(lhs, rhs, dimension_numbers, preferred_element_type,
                   configs):
  out = scaled_dot_impl(lhs, rhs, dimension_numbers, preferred_element_type,
                        configs)
  res = (lhs, rhs)
  return out, res

