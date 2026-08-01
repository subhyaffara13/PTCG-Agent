
def _ragged_dot_general_dtype_rule(
    lhs: Array,
    rhs: Array,
    group_sizes: Array,
    *,
    ragged_dot_dimension_numbers: RaggedDotDimensionNumbers,
    precision,
    preferred_element_type: DTypeLike | None,
    group_offset,
    out_sharding,
) -> np.dtype:
  if not dtypes.issubdtype(group_sizes.dtype, np.integer):
    raise TypeError(
        'ragged_dot_general requires that '
        'group_sizes.dtype is subtype of np.integer.'
    )
  # defer the output dtype to dot_general, which is part of the _ragged_dot_general_impl.
  return _dot_general_dtype_rule(
      lhs,
      rhs,
      dimension_numbers=ragged_dot_dimension_numbers.dot_dimension_numbers,
      precision=precision,
      preferred_element_type=preferred_element_type,
      out_sharding=None,
      name='lax.ragged_dot_general',
  )

