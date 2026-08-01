
def _scatter_addsub_lower_gpu(
    ctx, operand, indices, updates, *, update_jaxpr, update_consts,
    dimension_numbers, indices_are_sorted, unique_indices, mode,
    reduce_op):
  operand_aval_in, _, updates_aval_in = ctx.avals_in
  if operand_aval_in.dtype != np.complex128:
    return _scatter_lower(ctx, operand, indices, updates,
                          update_jaxpr=update_jaxpr,
                          update_consts=update_consts,
                          dimension_numbers=dimension_numbers,
                          indices_are_sorted=indices_are_sorted,
                          unique_indices=unique_indices, mode=mode)

  if mode == GatherScatterMode.CLIP:
    clip_fn = mlir.lower_fun(_clamp_scatter_indices, multiple_results=False)
    indices, = clip_fn(ctx.replace(avals_out=None), operand, indices, updates,
                       dnums=dimension_numbers)

  aval_out, = ctx.avals_out
  dnums = dimension_numbers
  scatter_dnums = hlo.ScatterDimensionNumbers.get(
      update_window_dims=list(dnums.update_window_dims),
      inserted_window_dims=list(dnums.inserted_window_dims),
      input_batching_dims=list(dnums.operand_batching_dims),
      scatter_indices_batching_dims=list(dnums.scatter_indices_batching_dims),
      scattered_dims_to_operand_dims=list(dnums.scatter_dims_to_operand_dims),
      index_vector_dim=len(ctx.avals_in[1].shape) - 1,
  )
  real_dtype = _real_dtype(aval_out.dtype)
  operand_type_part = mlir.aval_to_ir_type(
      ctx.module_context, core.ShapedArray(aval_out.shape, real_dtype))

  def _scatter(operand_part, updates_part):
    operand_part = [operand_part]
    updates_part = [updates_part]

    scatter = hlo.ScatterOp(
        (operand_type_part,), operand_part, indices, updates_part, scatter_dnums,
        indices_are_sorted=ir.BoolAttr.get(indices_are_sorted),
        unique_indices=ir.BoolAttr.get(unique_indices))
    scalar_type = mlir.aval_to_ir_type(ctx.module_context, core.ShapedArray((), real_dtype))
    reducer = scatter.regions[0].blocks.append(scalar_type, scalar_type)
    with ir.InsertionPoint(reducer):
      hlo.return_([reduce_op(*reducer.arguments).result])
    return mlir.lower_with_sharding_in_types(ctx, scatter.result, aval_out)

  real = _scatter(hlo.real(operand), hlo.real(updates))
  imag = _scatter(hlo.imag(operand), hlo.imag(updates))
  return [hlo.complex(real, imag)]

