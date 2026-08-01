
def _gather_lower(ctx, operand, indices, *,
                  dimension_numbers, slice_sizes, unique_indices,
                  indices_are_sorted, mode, fill_value):
  _, indices_aval = ctx.avals_in
  aval_out, = ctx.avals_out
  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    return [_gather_lower_opaque(
        ctx, operand, indices, dimension_numbers=dimension_numbers,
        slice_sizes=slice_sizes, unique_indices=unique_indices,
        indices_are_sorted=indices_are_sorted, mode=mode,
        fill_value=fill_value)]

  if mode == GatherScatterMode.FILL_OR_DROP:
    gather_fill_fn = mlir.lower_fun(_gather_fill, multiple_results=False)
    return gather_fill_fn(
        ctx, operand, indices,
        dimension_numbers=dimension_numbers, slice_sizes=slice_sizes,
        unique_indices=unique_indices, indices_are_sorted=indices_are_sorted,
        fill_value=fill_value, output_shape=aval_out.shape)

  assert mode in (GatherScatterMode.PROMISE_IN_BOUNDS,
                  GatherScatterMode.CLIP), mode
  dnums = hlo.GatherDimensionNumbers.get(
      collapsed_slice_dims=list(dimension_numbers.collapsed_slice_dims),
      operand_batching_dims=list(dimension_numbers.operand_batching_dims),
      start_indices_batching_dims=list(
          dimension_numbers.start_indices_batching_dims
      ),
      index_vector_dim=len(indices_aval.shape) - 1,
      offset_dims=list(dimension_numbers.offset_dims),
      start_index_map=list(dimension_numbers.start_index_map),
  )
  if not core.is_constant_shape(slice_sizes):
    slice_sizes = mlir.eval_dynamic_shape_as_tensor(ctx, slice_sizes)
    # TODO(burmako): Fix overly conservative type inference of DynamicGatherOp.
    # For now use the build_generic so that we can specify the result type.
    # return hlo.DynamicGatherOp(
    #     operand, indices, mlir.shape_tensor(slice_sizes),
    #     dnums, indices_are_sorted=ir.BoolAttr.get(indices_are_sorted)).results
    flat_results, _ = mlir.ir_tree_registry.flatten(mlir.aval_to_ir_types(ctx.module_context, aval_out))
    results = flat_results
    operands = [operand, indices, slice_sizes]
    attributes: dict[str, ir.Attribute] = {
        "dimension_numbers": dnums,
        "indices_are_sorted": ir.BoolAttr.get(indices_are_sorted)
    }
    return hlo.DynamicGatherOp.build_generic(
        results=results, operands=operands, attributes=attributes).results
  elif core.is_empty_shape(aval_out.shape):
    out = mlir.full_like_aval(ctx, 0, aval_out)
    return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]
  else:
    out = hlo.gather(operand, indices, dnums, mlir.dense_int_array(slice_sizes),
                     indices_are_sorted=ir.BoolAttr.get(indices_are_sorted))
    return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

