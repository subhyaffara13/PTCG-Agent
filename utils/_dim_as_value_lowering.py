
def _dim_as_value_lowering(ctx: mlir.LoweringRuleContext, *,
                           dim):
  res, = mlir.eval_dynamic_shape(ctx, (dim,))
  assert isinstance(res, mlir.ir.Value)
  out_type = mlir.aval_to_ir_type(ctx.module_context, ctx.avals_out[0])
  if out_type != res.type:
    return [mlir.hlo.convert(out_type, res)]
  else:
    return [res]


def _dim_as_value_lowering(ctx: LoweringRuleContext, *, dim):
  placeholder = ctx.lowering_context.dynamic_shape_replacement_fn((dim,))[0]
  return ir_constant(placeholder, mlir_type=_dtype_to_ir_type(jnp.int32))

