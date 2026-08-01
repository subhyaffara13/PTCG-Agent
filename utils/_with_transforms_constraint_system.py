
def _with_transforms_constraint_system(
    ctx: DerivationContext,
    op: mgpu.WithTransformsOp,
) -> ConstraintSystemDerivationRuleResult:
  source = ValueSite(op, VariableType.OPERAND, 0)
  dest = ValueSite(op, VariableType.RESULT, 0)
  var = ctx.producer_ref(source)
  tiling = _extract_smem_transforms_from_custom_transform_attrs(op.ref.type, op.transforms)
  if tiling.tiling is not None:
    if not cs.is_valid_assignment(var, tiling):
      raise ValueError(
          f"Cannot apply tiling {tiling.tiling} to memref with shape {source.shape}."
      )
  assignments: dict[cs.Variable, cs.Constant] = {var: tiling}
  return cs.ConstraintSystem(assignments=assignments), {var: [source, dest]}

