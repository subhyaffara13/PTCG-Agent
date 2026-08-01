
def _optimization_barrier_lowering_rule(ctx, *args):
  barrier_types = map(partial(mlir._aval_to_ir_types, ctx.module_context),
                      ctx.avals_in)
  flat_args, _ = mlir.ir_tree_registry.flatten(args)
  barrier_op = hlo.OptimizationBarrierOp(flat_args)
  _, treedef = mlir.ir_tree_registry.flatten(barrier_types)
  out = [mlir.lower_with_sharding_in_types(ctx, op, aval)
         for op, aval in zip(barrier_op.results, ctx.avals_out)]
  return treedef.unflatten(out)

