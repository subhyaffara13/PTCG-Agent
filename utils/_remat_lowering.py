
def _remat_lowering(
    ctx: mlir.LoweringRuleContext,
    *args,
    jaxpr: core.Jaxpr,
    prevent_cse: bool,
    differentiated: bool,
    policy,
):
  if isinstance(prevent_cse, bool):
    prevent_cse = (prevent_cse,) * len(ctx.avals_in)  # pyrefly: ignore[bad-assignment]
  assert isinstance(prevent_cse, tuple)
  if differentiated and any(prevent_cse):
    _, barrier_avals = partition_list(prevent_cse, ctx.avals_in)
    other_args, barrier_args = partition_list(prevent_cse, args)
    flat_barrier_args, _ = mlir.ir_tree_registry.flatten(barrier_args)
    barrier_op = hlo.OptimizationBarrierOp(flat_barrier_args)
    _, barrier_treedef = mlir.ir_tree_registry.flatten(
        [mlir._aval_to_ir_types(ctx.module_context, a) for a in barrier_avals])
    res = [mlir.lower_with_sharding_in_types(ctx, op, aval)
           for op, aval in zip(barrier_op.results, barrier_avals)]
    barrier_results = barrier_treedef.unflatten(res)
    args = merge_lists(prevent_cse, other_args, barrier_results)
  outs, tokens_out = mlir.jaxpr_subcomp(
      ctx.module_context, jaxpr, ctx.name_stack.extend('checkpoint'),
      ctx.tokens_in, (), *args, dim_var_values=ctx.dim_var_values,
      const_lowering=ctx.const_lowering, outer_traceback=ctx.traceback)
  ctx.set_tokens_out(tokens_out)
  return outs

