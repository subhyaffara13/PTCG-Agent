
def _reshape_lowering_rule(ctx: LoweringRuleContext, x, new_sizes, dimensions,
                           sharding):
  if dimensions is not None:
    raise NotImplementedError
  if any(d is None for d in new_sizes):
    raise NotImplementedError
  if not ctx.avals_in[0].shape:
    return vector.broadcast(ctx.aval_to_ir_type(ctx.avals_out[0]), x)
  if not ctx.avals_out[0].shape:
    return vector.extract(x, [], [0] * len(ctx.avals_in[0].shape))
  return vector.shape_cast(ctx.aval_to_ir_type(ctx.avals_out[0]), x)


def _reshape_lowering_rule(
    ctx: LoweringRuleContext, x, new_sizes, dimensions, sharding
):
  if dimensions is not None:
    raise NotImplementedError("Not implemented: dimensions")
  if sharding is not None:
    raise NotImplementedError("Not implemented: sharding")
  [x_aval] = ctx.avals_in
  return _ensure_fa(x, x_aval.dtype).reshape(new_sizes)


def _reshape_lowering_rule(
    ctx: LoweringRuleContext, a, *, new_sizes, dimensions, sharding,
):
  del new_sizes  # Unused.
  if dimensions is not None:
    return ValueError("`dimensions` is not supported.")

  a = _ensure_ir_value(a, *ctx.avals_in)
  [a_aval] = ctx.avals_in
  [out_aval] = ctx.avals_out
  # Triton Reshape doesn't support scalar result types (only 0d tensors).
  if out_aval.ndim == 0:
    return _reduce_lowering(jnp.add, ctx, a, axes=tuple(range(a_aval.ndim)))
  return _reshape(a, out_aval.shape)

