
def bcoo_dot_general_sampled(A: Array, B: Array, indices: Array, *, dimension_numbers: DotDimensionNumbers) -> Array:
  """A contraction operation with output computed at given sparse indices.

  Args:
    lhs: An ndarray.
    rhs: An ndarray.
    indices: BCOO indices.
    dimension_numbers: a tuple of tuples of the form
      `((lhs_contracting_dims, rhs_contracting_dims),
      (lhs_batch_dims, rhs_batch_dims))`.

  Returns:
    BCOO data, an ndarray containing the result.
  """
  (lhs_contract, rhs_contract), (lhs_batch, rhs_batch) = dimension_numbers
  cdims = (api_util._ensure_index_tuple(lhs_contract),
           api_util._ensure_index_tuple(rhs_contract))
  bdims = (api_util._ensure_index_tuple(lhs_batch),
           api_util._ensure_index_tuple(rhs_batch))
  return bcoo_dot_general_sampled_p.bind(A, B, indices,
                                         dimension_numbers=(cdims, bdims))

