
def scaled_dot_general_fn(lhs, rhs, dimension_numbers, preferred_element_type,
                          configs):
  return scaled_dot_impl(lhs, rhs, dimension_numbers, preferred_element_type,
                         configs)

