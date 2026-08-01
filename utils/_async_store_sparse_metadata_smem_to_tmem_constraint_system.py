
def _async_store_sparse_metadata_smem_to_tmem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncStoreSparseMetadataSmemToTmemOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  source_variable = ctx.producer_ref(source)
  destination = ValueSite(op, VariableType.OPERAND, 1)
  destination_variable = ctx.producer_ref(destination)
  return (
      cs.ConstraintSystem(
          assignments={
              destination_variable: cs.TMEMLayout(
                  tcgen05.sparse_meta_layout()
              ),
              source_variable: cs.SMEMTransforms(None),
          },
      ),
      {source_variable: [source], destination_variable: [destination]},
  )

