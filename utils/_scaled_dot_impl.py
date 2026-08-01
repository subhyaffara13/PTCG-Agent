
def _scaled_dot_impl(
    lhs: Array,
    rhs: Array,
    lhs_scale: Array,
    rhs_scale: Array,
    *,
    dimension_numbers: lax.DotDimensionNumbers,
    preferred_element_type: DTypeLike | None = None,
) -> Array:
  """Implementation of scaled_dot that could be replaced by XLA."""

  (lhs_contracting, rhs_contracting), _ = dimension_numbers

  lhs_scale = _scale_broadcast(lhs_scale, lhs.shape, lhs_contracting)
  lhs = lhs.astype(dtypes.bfloat16)
  lhs_scale = lhs_scale.astype(dtypes.bfloat16)
  lhs_scaled = lhs * lhs_scale

  rhs_scale = _scale_broadcast(rhs_scale, rhs.shape, rhs_contracting)
  rhs = rhs.astype(dtypes.bfloat16)
  rhs_scale = rhs_scale.astype(dtypes.bfloat16)
  rhs_scaled = rhs * rhs_scale

  result = jax.lax.dot_general(
      lhs_scaled,
      rhs_scaled,
      dimension_numbers=dimension_numbers,
      preferred_element_type=preferred_element_type,
  )

  return result

