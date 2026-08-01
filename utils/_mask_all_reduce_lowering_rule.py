
def _mask_all_reduce_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, x, *, reduce, kind: str
):
  [out_aval] = ctx.avals_out
  return tpu.all_reduce(
      ir.VectorType.get(
          out_aval.shape,
          ir.IntegerType.get_signless(32),
      ),
      x,
      0,
      ir.Attribute.parse(f"#tpu.reduction_kind<{kind}>"),
  )

