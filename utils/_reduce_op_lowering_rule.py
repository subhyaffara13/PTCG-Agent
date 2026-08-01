
def _reduce_op_lowering_rule(ctx: sc_lowering.LoweringRuleContext, x, axes,
                             *, reduction_kind, out_sharding=None):
  del out_sharding  # Unused.
  if axes != (0,):
    raise NotImplementedError(
        f"reductions require axes to be (0,) on SparseCore, but got {axes}.")
  vec_dim = ctx.avals_in[0].shape[0]
  i1t = ir.IntegerType.get_signless(1)
  c1 = arith.constant(i1t, ir.IntegerAttr.get(i1t, 1))
  x_shp = ctx.avals_in[0].shape
  c1v = vector.broadcast(ir.VectorType.get(x_shp, c1.type), c1)
  return vector.extract(
      _masked_cumop_lowering_rule(ctx, x, c1v, reduction_kind=reduction_kind),
      [], [vec_dim - 1])

