
def _bcoo_dot_general_sampled_transpose(ct, A, B, indices, *, dimension_numbers):
  A_shape = A.aval.shape if hasattr(A, 'aval') else A.shape
  B_shape = B.aval.shape if hasattr(B, 'aval') else B.shape
  mat_shape = _dot_general_validated_shape(A_shape, B_shape, dimension_numbers)
  mat = ad.UndefinedPrimal(core.ShapedArray(mat_shape, ct.dtype))
  indices, ct = _bcoo_extract_transpose(ct, indices, mat, assume_unique=True)
  kwds = {'dimension_numbers': dimension_numbers,
          'precision': None,
          'preferred_element_type': None,
          'out_sharding': None}
  A, B = ad.get_primitive_transpose(lax.dot_general_p)(ct, A, B, **kwds)
  return A, B, indices

