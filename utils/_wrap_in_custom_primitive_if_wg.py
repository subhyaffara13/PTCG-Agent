
def _wrap_in_custom_primitive_if_wg(
    ctx: LoweringRuleContext, operands: Sequence[ir.Value]
):
  """Wraps the body in a CustomPrimitiveOp for warpgroup semantics.

  For warpgroup lowering semantics, yields remapped block arguments that
  should be used instead of the original operands, and temporarily switches
  the lowering semantics to Lane for the duration of the context. For lane
  semantics, yields the original operands unchanged.
  """
  if ctx.module_ctx.lowering_semantics == mgpu.LoweringSemantics.Warpgroup:
    custom_op = mgpu.dialect.CustomPrimitiveOp(
        result=[],
        operands_=list(operands),
        in_layouts=[],
        in_transforms=[],
        out_layouts=[],
    )
    block = custom_op.body.blocks.append(*[o.type for o in operands])
    with ir.InsertionPoint(block):
      ctx.module_ctx.lowering_semantics = mgpu.LoweringSemantics.Lane
      try:
        yield list(block.arguments)
      finally:
        ctx.module_ctx.lowering_semantics = mgpu.LoweringSemantics.Warpgroup
      mgpu.dialect.ReturnOp(operands_=[])
    _isolate_from_above(custom_op)
  else:
    yield list(operands)

