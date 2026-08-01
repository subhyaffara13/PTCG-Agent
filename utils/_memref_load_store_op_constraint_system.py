
def _memref_load_store_op_constraint_system(
    ctx: DerivationContext,
    op: memref.LoadOp | memref.StoreOp,
) -> ConstraintSystemDerivationRuleResult:
  del ctx

  ref_shape = ir.MemRefType(op.memref.type).shape
  if ref_shape and ref_shape != [1]:
    raise NotImplementedError(
        f"Only scalar memrefs are supported, got {ref_shape}"
    )

  ref_op_index = 0 if isinstance(op, memref.LoadOp) else 1
  ref = ValueSite(op, VariableType.OPERAND, ref_op_index)
  var = cs.Variable(ref)
  assignments: dict[cs.Variable, cs.Constant] = {var: cs.SMEMTransforms(None)}
  return cs.ConstraintSystem(assignments=assignments), {var: [ref]}

