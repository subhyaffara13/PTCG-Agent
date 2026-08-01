
def _griddepcontrol_launch_dependents_lowering(
    ctx: lowering.LoweringRuleContext,
):
  void = ir.Type.parse("!llvm.void")
  with lowering._wrap_in_custom_primitive_if_wg(ctx, []):
    llvm_dialect.inline_asm(
        void, [], "griddepcontrol.launch_dependents;", "", has_side_effects=True
    )
  return ()

