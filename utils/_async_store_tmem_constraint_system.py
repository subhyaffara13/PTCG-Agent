
def _async_store_tmem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncStoreTmemOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  source_variable = cs.Variable(source)
  destination = ValueSite(op, VariableType.OPERAND, 1)
  destination_variable = ctx.producer_ref(destination)
  constraint = cs.IsTransferableTmemRegisters(
      source_variable,
      destination_variable,
      tuple(ir.ShapedType(op.source.type).shape),
      bitwidth=utils.bitwidth(op.source.type.element_type),
  )
  return (
      cs.ConstraintSystem(constraints=[constraint]),
      {source_variable: [source], destination_variable: [destination]},
  )

