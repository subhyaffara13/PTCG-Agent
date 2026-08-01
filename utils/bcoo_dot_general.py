
def bcoo_dot_general(lhs: BCOO | Array, rhs: BCOO | Array, *,
                     dimension_numbers: DotDimensionNumbers,
                     precision: None = None,
                     preferred_element_type: None = None,
                     out_sharding=None) -> BCOO | Array:
  """A general contraction operation.

  Args:
    lhs: An ndarray or BCOO-format sparse array.
    rhs: An ndarray or BCOO-format sparse array..
    dimension_numbers: a tuple of tuples of the form
      `((lhs_contracting_dims, rhs_contracting_dims),
      (lhs_batch_dims, rhs_batch_dims))`.
    precision: unused
    preferred_element_type: unused

  Returns:
    An ndarray or BCOO-format sparse array containing the result. If both inputs
    are sparse, the result will be sparse, of type BCOO. If either input is dense,
    the result will be dense, of type ndarray.
  """
  # TODO(jakevdp) make use of these?
  del precision, out_sharding  # unused
  if isinstance(lhs, BCOO) and isinstance(rhs, BCOO):
    shape = _dot_general_validated_shape(lhs.shape, rhs.shape,
                                         dimension_numbers)
    bufs = _bcoo_spdot_general(lhs.data, lhs.indices, rhs.data, rhs.indices,
                               lhs_spinfo=lhs._info, rhs_spinfo=rhs._info,
                               dimension_numbers=dimension_numbers,
                               preferred_element_type=preferred_element_type)
    return BCOO(bufs, shape=shape)
  elif isinstance(lhs, BCOO):
    assert not isinstance(rhs, BCOO)
    return _bcoo_dot_general(lhs.data, lhs.indices, rhs, dimension_numbers=dimension_numbers,
                             preferred_element_type=preferred_element_type,
                             lhs_spinfo=lhs._info)
  elif isinstance(rhs, BCOO):
    return _bcoo_rdot_general(lhs, rhs.data, rhs.indices, dimension_numbers=dimension_numbers,
                              preferred_element_type=preferred_element_type,
                              rhs_spinfo=rhs._info)
  else:
    return lax.dot_general(lhs, rhs, dimension_numbers=dimension_numbers,
                           preferred_element_type=preferred_element_type)

