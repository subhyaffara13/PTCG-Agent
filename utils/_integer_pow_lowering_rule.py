
def _integer_pow_lowering_rule(ctx: LoweringRuleContext, x, *, y):
  return lower_fun(lax_internal._integer_pow)(ctx, x, y=y)


def _integer_pow_lowering_rule(ctx: LoweringRuleContext, x, y):
  [x_aval] = ctx.avals_in
  if y == -1:
    return _lower_fun(lambda x: 1 / x)(ctx, x)
  if y <= 1:
    raise NotImplementedError

  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Lane:
    mul_op = operator.mul
  elif jnp.issubdtype(x_aval.dtype, jnp.integer):
    mul_op = arith_dialect.muli
  elif jnp.issubdtype(x_aval.dtype, jnp.floating):
    mul_op = arith_dialect.mulf
  else:
    raise NotImplementedError(f"Unsupported dtype {x_aval.dtype}")

  # Y is an integer. Here we start with res = x so the range is y-1
  res = x
  # Repeated doubling algorithm.
  for i in reversed(range(y.bit_length() - 1)):
    res = mul_op(res, res)
    if (y >> i) & 1:
      res = mul_op(res, x)
  return res

