
def _fused_lowering(ctx, *args, out_spaces, jaxpr):
  const_args_and_avals = core.jaxpr_const_args(jaxpr.jaxpr)
  const_args, const_arg_avals = unzip2(const_args_and_avals)
  const_arg_values, _ = mlir.ir_tree_registry.flatten([
      mlir.ir_constants(c, const_lowering=ctx.const_lowering, aval=aval)
      for c, aval in const_args_and_avals
  ])
  in_avals = [*const_arg_avals, *ctx.avals_in]
  func_op, _, _ = mlir.lower_called_computation(
      "fused", jaxpr, ctx.module_context, len(const_args), in_avals,
      ctx.avals_out, ctx.tokens_in)
  out_spaces_ = [ir.StringAttr.get(str(s)) for s in out_spaces]
  flat_ops, _ = mlir.ir_tree_registry.flatten([*const_arg_values, *args])
  fused = mlir.custom_call(
      "fused",
      result_types=func_op.type.results,
      operands=flat_ops,
      called_computations=[func_op.name.value],
      backend_config=dict(out_spaces=ir.ArrayAttr.get(out_spaces_),
                          inlineable=ir.BoolAttr.get(False),
                          MUST_FUSE=ir.BoolAttr.get(True)),
  )
  return fused.results

