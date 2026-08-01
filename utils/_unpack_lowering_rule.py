
def _unpack_lowering_rule(
    ctx: sc_lowering.LoweringRuleContext, ab, *, format, preferred_element_type
):
  del preferred_element_type  # Unused.
  out_aval, _ = ctx.avals_out
  out_type = ctx.aval_to_ir_type(out_aval)
  return (
      tpu.unpack_subelements(out_type, ab, 0, _format_to_ir_attribute(format)),
      tpu.unpack_subelements(out_type, ab, 1, _format_to_ir_attribute(format)),
  )

