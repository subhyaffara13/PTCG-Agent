
def _scaled_matmul_abstract(a, b, a_scale, b_scale, *, preferred_element_type):
  batch, non_contracting_lhs, contracting_lhs = a.shape
  _, non_contracting_rhs, _ = b.shape
  output_shape = (batch, non_contracting_lhs, non_contracting_rhs)
  return (core.ShapedArray(output_shape, preferred_element_type),)

