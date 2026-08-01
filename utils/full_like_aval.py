
def full_like_aval(ctx: LoweringRuleContext, value, aval: core.ShapedArray) -> ir.Value:
  """Returns an IR constant shaped full of `value` shaped like `aval`."""
  zero = ir_constant(np.array(value, aval.dtype))
  return broadcast_in_dim(ctx, zero, aval, broadcast_dimensions=())

