
def _parallel_loop_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext,
    *flat_args,
    tree,
    unroll,
    jaxpr,
):
  lower, upper, step, consts, carry = tree.unflatten(flat_args)
  for_op = scf.ForOp(
      _ensure_ir_value(lower, pallas_core.index_map_grid_aval),
      _ensure_ir_value(upper, pallas_core.index_map_grid_aval),
      _ensure_ir_value(step, pallas_core.index_map_grid_aval),
      carry,
  )
  for_op.attributes["sc.parallel_access"] = ir.UnitAttr.get()
  for_op.attributes["sc.loop_unroll_factor"] = ir.IntegerAttr.get(
      ir.IntegerType.get_signless(64), unroll
  )
  with ir.InsertionPoint(for_op.body):
    _, _, _, consts_block_shapes, *_ = tree.unflatten(ctx.block_shapes)
    lowering_ctx = ctx.lowering_context.replace(
        block_shapes=[*consts_block_shapes, None] + [None] * len(carry),
    )
    carry_out = tc_lowering.jaxpr_subcomp(
        lowering_ctx,
        pe.convert_constvars_jaxpr(jaxpr),
        *consts,
        for_op.induction_variable,
        *for_op.inner_iter_args,
    )
    scf.yield_(carry_out)
  return for_op.results

