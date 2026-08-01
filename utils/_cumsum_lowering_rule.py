
def _cumsum_lowering_rule(ctx: sc_lowering.LoweringRuleContext, x, axis,
                          reverse):
  if axis != 0:
    raise NotImplementedError(f"SC cumsum: axis={axis} must be 0.")
  if len(ctx.avals_in[0].shape) != 1:
    raise NotImplementedError(f"SC cumsum: x={ctx.avals_in[0]} must be rank 1")
  if reverse:
    raise NotImplementedError("SC cumsum: reverse=True is not yet supported")
  i1t = ir.IntegerType.get_signless(1)
  c1 = arith.constant(i1t, ir.IntegerAttr.get(i1t, 1))
  c1v = vector.broadcast(ir.VectorType.get(x.type.shape, c1.type), c1)
  return tpu.scan(
      x.type, x, ir.Attribute.parse("#tpu.reduction_kind<sum>"), mask=c1v)


def _cumsum_lowering_rule(
    ctx: LoweringRuleContext, x, *, axis: int, reverse: bool
):
  if reverse:
    raise NotImplementedError("Reverse cumsum is not supported.")
  return _associative_scan_lowering(jnp.add, ctx, x, (axis,))[0]

