
def _ragged_dot_general_lower(
    ctx,
    lhs,
    rhs,
    group_sizes,
    *,
    ragged_dot_dimension_numbers,
    precision,
    preferred_element_type: np.dtype | None,
    group_offset: Array | None = None,
    out_sharding=None,
    platform: str = 'default',
):
  if group_offset is not None:
    raise NotImplementedError('Unimplemented group_offset support.')

  if jaxlib_extension_version < 459:
    if any(not core.is_constant_shape(aval.shape) for aval in ctx.avals_in):
      raise NotImplementedError(
          'ragged_dot is not supported with dynamic shapes in this version '
          'of jaxlib. Please update jaxlib to a newer version.')
  if not config.jax_ragged_dot_use_ragged_dot_instruction.value:
    return mlir.lower_fun(_ragged_dot_general_impl, multiple_results=False)(
        ctx, lhs, rhs, group_sizes,
        ragged_dot_dimension_numbers=ragged_dot_dimension_numbers,
        precision=precision,
        preferred_element_type=preferred_element_type,
        group_offset=group_offset,
        out_sharding=out_sharding,
    )

  del preferred_element_type  # Implied by the output aval
  lhs, rhs, accumulation_aval, _ = _handle_dot_precision(
      ctx, lhs, rhs, precision, platform
  )
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = (
      ragged_dot_dimension_numbers.dot_dimension_numbers
  )
  rhs_group_dims = ragged_dot_dimension_numbers.rhs_group_dimensions
  ragged_dot_dnums = chlo.RaggedDotDimensionNumbers.get(
      lhs_batching_dimensions=list(lhs_batch),
      rhs_batching_dimensions=list(rhs_batch),
      lhs_contracting_dimensions=list(lhs_contracting),
      rhs_contracting_dimensions=list(rhs_contracting),
      lhs_ragged_dimensions=list(
          ragged_dot_dimension_numbers.lhs_ragged_dimensions
      ),
      rhs_group_dimensions=list(rhs_group_dims),
  )
  acc_type = mlir.aval_to_ir_type(ctx.module_context, accumulation_aval)
  result = chlo.ragged_dot(
      acc_type,
      lhs,
      rhs,
      group_sizes,
      ragged_dot_dnums,
      precision_config=chlo_precision_attr(precision),
  )
  (aval_out,) = ctx.avals_out
  result = mlir.lower_with_sharding_in_types(ctx, result, aval_out)
  if accumulation_aval.dtype != aval_out.dtype:
    result = mlir.convert_hlo(ctx, result, accumulation_aval, aval_out)
  return [result]

