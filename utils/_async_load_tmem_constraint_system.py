
def _async_load_tmem_constraint_system(
    ctx: DerivationContext,
    op: mgpu.AsyncLoadTmemOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  source_variable = ctx.producer_ref(source)
  destination = ValueSite(op, VariableType.RESULT, 0)
  destination_variable = cs.Variable(destination)
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

