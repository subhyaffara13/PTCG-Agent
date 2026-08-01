
def multi_broadcast_in_dim(ctx: LoweringRuleContext,
                           ops: Sequence[ir.Value],
                           ops_avals: Sequence[core.AbstractValue],
                           out_shape: core.Shape,
                           out_sharding) -> Sequence[ir.Value]:
  """Broadcasts multiple ops to the out_shape."""
  out = []
  for op, op_aval in zip(ops, ops_avals):
    op_aval_shape = op_aval.shape  # pyrefly: ignore[missing-attribute]
    op_aval_sharding = op_aval.sharding  # pyrefly: ignore[missing-attribute]
    out_aval = core.ShapedArray(
        out_shape, op_aval.dtype, sharding=out_sharding)  # pyrefly: ignore[missing-attribute]
    if core.definitely_equal_shape(op_aval_shape, out_shape):
      if op_aval_sharding.spec.unreduced or op_aval_sharding.spec.reduced:
        out.append(op)
      elif op_aval_sharding == out_sharding:
        out.append(op)
      else:
        out.append(lower_with_sharding_in_types(ctx, op, out_aval))
    else:
      if op_aval_sharding.spec.unreduced:
        raise NotImplementedError()
      assert len(op_aval_shape) <= len(out_shape), (op_aval_shape, out_shape)
      broadcast_dimensions = list(range(len(out_shape) - len(op_aval_shape), len(out_shape)))
      b_out = broadcast_in_dim(
          ctx, op, out_aval, broadcast_dimensions=broadcast_dimensions)
      b_out = lower_with_sharding_in_types(ctx, b_out, out_aval)
      out.append(b_out)
  return out

