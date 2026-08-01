
def bcsr_dot_general(lhs: BCSR | Array, rhs: Array, *,
                     dimension_numbers: DotDimensionNumbers,
                     precision: None = None,
                     preferred_element_type: None = None,
                     out_sharding=None) -> Array:
  """A general contraction operation.

  Args:
    lhs: An ndarray or BCSR-format sparse array.
    rhs: An ndarray or BCSR-format sparse array..
    dimension_numbers: a tuple of tuples of the form
      `((lhs_contracting_dims, rhs_contracting_dims),
      (lhs_batch_dims, rhs_batch_dims))`.
    precision: unused
    preferred_element_type: unused

  Returns:
    An ndarray or BCSR-format sparse array containing the result. If both inputs
    are sparse, the result will be sparse, of type BCSR. If either input is
    dense, the result will be dense, of type ndarray.
  """
  del precision, out_sharding  # unused
  if isinstance(rhs, (np.ndarray, jax.Array)):
    if isinstance(lhs, (np.ndarray, jax.Array)):
      return lax.dot_general(lhs, rhs, dimension_numbers=dimension_numbers,
                             preferred_element_type=preferred_element_type)

    if isinstance(lhs, BCSR):
      lhs_data, lhs_indices, lhs_indptr = lhs._bufs
      return _bcsr_dot_general(lhs_data, lhs_indices, lhs_indptr, rhs,
                               dimension_numbers=dimension_numbers,
                               preferred_element_type=preferred_element_type,
                               lhs_spinfo=lhs._info)

  raise NotImplementedError("bcsr_dot_general currently implemented for BCSR "
                            "lhs and ndarray rhs.")

