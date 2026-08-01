
def _async_store_scales_smem_to_tmem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncStoreScalesSmemToTmemOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  source_variable = ctx.producer_ref(source)
  destination = ValueSite(op, VariableType.OPERAND, 1)
  destination_variable = ctx.producer_ref(destination)

  assignments: dict[cs.Variable, cs.Constant] = {
      source_variable: cs.SMEMTransforms(None)
  }
  k_tiles = destination.shape[1] // 4
  if source.shape == (1, k_tiles, 64, 16):
    assignments[destination_variable] = cs.TMEMLayout(
        tcgen05.b_scales_m64_collective_layout()
    )
  else:
    assignments[destination_variable] = cs.TMEMLayout(tcgen05.scales_layout())
  return (
      cs.ConstraintSystem(assignments),
      {source_variable: [source], destination_variable: [destination]},
  )

