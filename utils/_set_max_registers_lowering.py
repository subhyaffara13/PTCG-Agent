
def _set_max_registers_lowering(
    ctx: lowering.LoweringRuleContext, n, *, action
):
  del ctx
  nvvm_dialect.setmaxregister(
      n,
      nvvm_dialect.SetMaxRegisterAction.increase
      if action == "increase"
      else nvvm_dialect.SetMaxRegisterAction.decrease,
  )
  return ()

