
def _scaled_matmul(
    lhs: Array,
    rhs: Array,
    lhs_scales: Array,
    rhs_scales: Array,
    preferred_element_type: DTypeLike = np.dtype('float32'),
  ) -> Array:
  output = _scaled_matmul_p_wrapper.bind(
      lhs, rhs, lhs_scales, rhs_scales,
      preferred_element_type=preferred_element_type
  )
  return output[0]

