
def _rev_lowering_rule(ctx: LoweringRuleContext, x, dimensions):
  del ctx  # Unused.
  if dimensions != (0,):
    raise NotImplementedError(f"Invalid dimensions for SC lax.rev: {dimensions}")
  i32 = ir.IntegerType.get_signless(32)
  vec_dim = sc_core.get_sparse_core_info().num_lanes
  cdim = arith.constant(i32, ir.IntegerAttr.get(i32, vec_dim - 1))
  cdim_vec = vector.broadcast(ir.VectorType.get((vec_dim,), cdim.type), cdim)
  return tpu.dynamic_gather(
      x,
      arith.subi(cdim_vec, tpu.iota(cdim_vec.type, dimensions=[0])),
      dimensions=[0],
  )

