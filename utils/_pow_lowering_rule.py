
def _pow_lowering_rule(ctx: LoweringRuleContext, x, y):
  # jax accepts float base (x) and integer/float exponent (y), and integer
  # exponent is casted to float.
  out_type = ctx.aval_to_ir_type(ctx.avals_out[0])
  if jnp.issubdtype(ctx.avals_in[1].dtype, jnp.unsignedinteger):
    y = arith.uitofp(out_type, y)
  elif jnp.issubdtype(ctx.avals_in[1].dtype, jnp.signedinteger):
    y = arith.sitofp(out_type, y)
  if not isinstance(x, ir.Value) and x == 2.:
    return mlir_math.exp2(y)
  x, y = _bcast(
      x,
      y,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  return mlir_math.powf(x, y)

