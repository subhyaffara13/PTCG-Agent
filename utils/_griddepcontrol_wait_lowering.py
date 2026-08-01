
def _griddepcontrol_wait_lowering(ctx: lowering.LoweringRuleContext):
  void = ir.Type.parse("!llvm.void")
  with lowering._wrap_in_custom_primitive_if_wg(ctx, []):
    llvm_dialect.inline_asm(
        void, [], "griddepcontrol.wait;", "", has_side_effects=True
    )
  return ()

