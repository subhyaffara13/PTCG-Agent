
def _scatter_lower(ctx: mlir.LoweringRuleContext, operand, indices, updates, *,
                   update_jaxpr: core.Jaxpr, update_consts, dimension_numbers,
                   indices_are_sorted, unique_indices, mode):
  avals_in = lax_utils.ensure_shaped(*ctx.avals_in)
  aval_out, = lax_utils.ensure_shaped(*ctx.avals_out)
  if update_jaxpr is None:
    assert not update_consts
    operand_dtype = avals_in[0].dtype
    update_jaxpr, update_consts = lax._reduction_jaxpr(
        _scatter_reduction_computation, core.ShapedArray((), operand_dtype))

  if dtypes.issubdtype(aval_out.dtype, dtypes.extended):
    return [_scatter_lower_opaque(
        ctx, operand, indices, updates,
        update_jaxpr=update_jaxpr, update_consts=update_consts,
        dimension_numbers=dimension_numbers, unique_indices=unique_indices,
        indices_are_sorted=indices_are_sorted, mode=mode)]

  if mode == GatherScatterMode.CLIP:
    clip_fn = mlir.lower_fun(_clamp_scatter_indices, multiple_results=False)
    (indices,) = clip_fn(ctx.replace(avals_out=None), operand, indices,
                          updates, dnums=dimension_numbers)

  dnums = dimension_numbers
  scatter_dnums = hlo.ScatterDimensionNumbers.get(
      update_window_dims=list(dnums.update_window_dims),
      inserted_window_dims=list(dnums.inserted_window_dims),
      input_batching_dims=list(dnums.operand_batching_dims),
      scatter_indices_batching_dims=list(dnums.scatter_indices_batching_dims),
      scattered_dims_to_operand_dims=list(dnums.scatter_dims_to_operand_dims),
      index_vector_dim=len(avals_in[1].shape) - 1,
  )
  result = mlir.aval_to_ir_type(ctx.module_context, aval_out)
  operand = [operand]
  updates = [updates]
  op = hlo.ScatterOp((result,), operand, indices, updates, scatter_dnums,
                     indices_are_sorted=ir.BoolAttr.get(indices_are_sorted),
                     unique_indices=ir.BoolAttr.get(unique_indices))
  scalar_type = mlir.aval_to_ir_type(ctx.module_context, core.ShapedArray((), aval_out.dtype))
  update = op.update_computation.blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(update):
    name_stack = source_info_util.new_name_stack()
    if update_jaxpr.effects:
      raise NotImplementedError('Cannot lower effectful `scatter`.')
    out_nodes, _ = mlir.jaxpr_subcomp(
        ctx.module_context, update_jaxpr, name_stack, mlir.TokenSet(),
        update_consts, update.arguments[0], update.arguments[1],
        dim_var_values=ctx.dim_var_values, const_lowering=ctx.const_lowering,
        outer_traceback=ctx.traceback)
    flat_out_nodes, _ = mlir.ir_tree_registry.flatten(out_nodes)
    hlo.return_(flat_out_nodes)
  return [mlir.lower_with_sharding_in_types(ctx, r, aval)
          for r, aval in safe_zip(op.results, ctx.avals_out)]

