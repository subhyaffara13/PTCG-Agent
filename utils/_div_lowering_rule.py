
def _div_lowering_rule(ctx: LoweringRuleContext, x, y):
  x, y = _bcast(
      x,
      y,
      ctx.avals_in[0],
      ctx.avals_in[1],
      ctx.avals_out[0],
      ctx.lowering_context.dynamic_shape_replacement_fn,
  )
  (aval_out,) = ctx.avals_out
  if jnp.issubdtype(aval_out.dtype, jnp.signedinteger):
    return arith.divsi(x, y)
  if jnp.issubdtype(aval_out.dtype, jnp.unsignedinteger):
    return arith.divui(x, y)
  elif jnp.issubdtype(aval_out.dtype, jnp.floating):
    return arith.divf(x, y)
  raise NotImplementedError(aval_out.dtype)


def _div_lowering_rule(ctx: LoweringRuleContext, x, y):
  x_aval, y_aval = ctx.avals_in
  x, y = _bcast(x, y, *ctx.avals_in, *ctx.avals_out)
  signed = jnp.issubdtype(x_aval.dtype, jnp.signedinteger) or jnp.issubdtype(
      y_aval.dtype, jnp.signedinteger
  )
  if jnp.issubdtype(x_aval.dtype, np.floating) or jnp.issubdtype(
      y_aval.dtype, np.floating
  ):
    return _truediv(x, y, signed=signed)
  return _floordiv(x, y, signed=signed)

