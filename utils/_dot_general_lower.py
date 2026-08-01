
def _dot_general_lower(ctx, lhs, rhs, *, dimension_numbers,
                       precision, preferred_element_type: np.dtype | None,
                       out_sharding, platform: str = "default"):
  del preferred_element_type  # Implied by the output aval
  lhs, rhs, accumulation_aval, algorithm_kwarg = _handle_dot_precision(
      ctx, lhs, rhs, precision, platform
  )
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = dimension_numbers
  dot_dnums = hlo.DotDimensionNumbers.get(
      lhs_batching_dimensions=list(lhs_batch),
      rhs_batching_dimensions=list(rhs_batch),
      lhs_contracting_dimensions=list(lhs_contracting),
      rhs_contracting_dimensions=list(rhs_contracting))
  acc_type = mlir.aval_to_ir_type(ctx.module_context, accumulation_aval)
  result = hlo.dot_general(
      acc_type,
      lhs,
      rhs,
      dot_dnums,
      precision_config=precision_attr(precision),
      **algorithm_kwarg,
  )
  aval_out, = ctx.avals_out
  result = mlir.lower_with_sharding_in_types(ctx, result, aval_out)
  if accumulation_aval.dtype != aval_out.dtype:
    result = mlir.convert_hlo(ctx, result, accumulation_aval, aval_out)
  return [result]

