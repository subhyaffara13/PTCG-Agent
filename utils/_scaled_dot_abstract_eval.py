
def _scaled_dot_abstract_eval(
    lhs,
    rhs,
    lhs_scale,
    rhs_scale,
    *,
    dimension_numbers: lax.DotDimensionNumbers,
    preferred_element_type: DTypeLike | None = None,
):
  _scaled_dot_validate_inputs(
      lhs,
      rhs,
      lhs_scale,
      rhs_scale,
      dimension_numbers=dimension_numbers,
      preferred_element_type=preferred_element_type,
  )
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  lhs_shape, rhs_shape = lhs.shape, rhs.shape

  batch_dims_shape = [lhs_shape[i] for i in lhs_batch]

  lhs_kept = sorted(
      i
      for i in range(len(lhs_shape))
      if i not in lhs_contracting and i not in lhs_batch
  )
  rhs_kept = sorted([
      i
      for i in range(len(rhs_shape))
      if i not in rhs_contracting and i not in rhs_batch
  ])
  output_shape = tuple(
      batch_dims_shape
      + [lhs_shape[i] for i in lhs_kept]
      + [rhs_shape[i] for i in rhs_kept]
  )

  if preferred_element_type is not None:
    output_dtype = preferred_element_type
  else:
    output_dtype = dtypes.bfloat16

  return core.ShapedArray(output_shape, output_dtype)

