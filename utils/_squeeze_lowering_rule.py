
def _squeeze_lowering_rule(ctx: LoweringRuleContext, x, dimensions):
  del dimensions  # Unused.
  (aval_in,) = ctx.avals_in
  (aval_out,) = ctx.avals_out
  if not aval_out.shape:
    if aval_out.dtype.itemsize != 4:
      raise ValueError(
          "Only arrays with 32-bit element types can be converted to scalars,"
          f" but got: {aval_out.dtype}. Try casting the input before squeezing"
          " the scalar."
      )
    return vector.extract(x, [], [0] * len(aval_in.shape))
  return vector.shape_cast(ctx.aval_to_ir_type(ctx.avals_out[0]), x)


def _squeeze_lowering_rule(ctx: LoweringRuleContext, x, dimensions):
  [x_aval] = ctx.avals_in
  [y_aval] = ctx.avals_out
  return _ensure_fa(x, x_aval.dtype).reshape(y_aval.shape)


def _squeeze_lowering_rule(ctx: LoweringRuleContext, a, *, dimensions):
  del dimensions
  return _reshape_lowering_rule(ctx, a, new_sizes=None, dimensions=None, sharding=None)

