
def _async_store_smem_to_tmem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncStoreSmemToTmemOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  source_variable = ctx.producer_ref(source)
  destination = ValueSite(op, VariableType.OPERAND, 1)
  destination_variable = ctx.producer_ref(destination)
  bitwidth = utils.bitwidth(op.destination.type.element_type)
  packing = 32 // bitwidth
  tmem_layout = cs.TMEMLayout(tcgen05.tmem_default_layout(packing))
  if not cs.is_valid_assignment(destination_variable, tmem_layout):
    raise ValueError(
        f"Cannot assign TMEM layout {tmem_layout.value} to a TMEM ref "
        f"with shape {destination.shape}"
    )
  return (
      cs.ConstraintSystem(
          assignments={destination_variable: tmem_layout},
          constraints=[
              cs.IsValidMmaTiling(source_variable, bitwidth, allow_unswizzled=True)
          ],
      ),
      {source_variable: [source], destination_variable: [destination]},
  )

