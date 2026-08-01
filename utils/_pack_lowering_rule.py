
def _pack_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext,
    a,
    b,
    *,
    format,
    preferred_element_type,
):
  del preferred_element_type  # Unused.
  [out_aval] = ctx.avals_out
  return tpu.pack_subelements(
      ctx.aval_to_ir_type(out_aval),
      [a, b],
      [0, 1],
      _format_to_ir_attribute(format),
  )

