
def _integer_pow_rule(ctx: LoweringRuleContext, x, *, y: int):
  if y == 0:
    return _ones_like(x)

  is_reciprocal = y < 0
  if is_reciprocal:
    y = -y

  acc: ir.Value | None = None
  while y > 0:
    y, mod = divmod(y, 2)
    if mod:
      acc = x if acc is None else _mul(acc, x)
    if y > 0:
      x = _mul(x, x)
  assert acc is not None

  [x_aval] = ctx.avals_in
  [out_aval] = ctx.avals_out
  acc = _cast(acc, x_aval.dtype, out_aval.dtype)
  if is_reciprocal:
    signed = jnp.issubdtype(out_aval.dtype, jnp.signedinteger)
    return  _truediv(_ones_like(acc), acc, signed=signed)
  else:
    return acc

