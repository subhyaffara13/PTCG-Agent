
def _min_lowering_rule(ctx: LoweringRuleContext, x, y):
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
    return arith.minsi(x, y)
  elif jnp.issubdtype(aval_out.dtype, jnp.unsignedinteger):
    return arith.minui(x, y)
  elif jnp.issubdtype(aval_out.dtype, jnp.floating):
    return arith.minimumf(x, y)
  raise NotImplementedError(aval_out.dtype)


def _min_lowering_rule(ctx: LoweringRuleContext, x, y):
  # TODO(slebedev): Consider allowing customizing nan behavior.
  x_aval, y_aval = ctx.avals_in
  x, y = _bcast(x, y, *ctx.avals_in, *ctx.avals_out)
  if jnp.issubdtype(x_aval.dtype, jnp.floating):
    # TODO(slebedev): Triton promotes bfloat16 to float32 and back here.
    return arith_dialect.minnumf(x, y)
  if not jnp.issubdtype(x_aval.dtype, jnp.integer):
    raise NotImplementedError(
        f"unsupported dtypes: {x_aval.dtype} and {y_aval.dtype}"
    )
  if jnp.issubdtype(x_aval.dtype, jnp.signedinteger):
    return arith_dialect.minsi(x, y)
  else:
    return arith_dialect.minui(x, y)

