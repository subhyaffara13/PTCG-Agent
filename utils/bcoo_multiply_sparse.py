
def bcoo_multiply_sparse(lhs: BCOO, rhs: BCOO) -> BCOO:
  """An element-wise multiplication of two sparse arrays.

  Args:
    lhs: A BCOO-format array.
    rhs: A BCOO-format array.

  Returns:
    An BCOO-format array containing the result.
  """
  out_data, out_indices, out_shape = _bcoo_multiply_sparse(
      lhs.data, lhs.indices, rhs.data, rhs.indices, lhs_spinfo=lhs._info,
      rhs_spinfo=rhs._info)
  return BCOO((out_data, out_indices), shape=out_shape)

