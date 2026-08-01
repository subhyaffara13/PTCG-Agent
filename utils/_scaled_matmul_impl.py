
def _scaled_matmul_impl(a, b, a_scale, b_scale, preferred_element_type):
  return _scaled_matmul_p.bind(
      a, b, a_scale, b_scale, preferred_element_type=preferred_element_type
  )

