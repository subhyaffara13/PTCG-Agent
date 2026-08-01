
def _custom_primitive_constraint_system(
    ctx: DerivationContext,
    op: mgpu.CustomPrimitiveOp,
) -> ConstraintSystemDerivationRuleResult:
  assignments: dict[cs.Variable, cs.Constant] = {}
  constraints: list[cs.Constraint] = []
  in_layouts = iter(op.in_layouts)
  in_transforms = iter(op.in_transforms)
  variables: list[cs.Variable] = []
  for i, operand in enumerate(op.operands):
    if is_vector(operand):
      v = cs.Variable(ValueSite(op, VariableType.OPERAND, i))
      variables.append(v)
      assignments[v] = cs.RegisterLayout(
          layouts_lib.from_layout_attr(next(in_layouts))
      )
    elif _is_smem_ref(operand):
      # Here we need to create a new variable, even though it is equal to the
      # source operand. This is because we directly assign the new variable and
      # if we did that to the source there could be conflicting assignments.
      # For example, the same ref could be passed into the custom op twice with
      # different transforms, which needs to yield an unsatisfiable system.
      #
      # TODO(b/447079781): Consider creating the final constraint system using
      # __and__ and potentially returning Unsatisfiable() directly if there is
      # a conflict between the assignments.
      value_site = ValueSite(op, VariableType.OPERAND, i)
      source_var = ctx.producer_ref(value_site)
      v = cs.Variable(value_site)
      constraints.append(cs.Equals(lhs=source_var, rhs=v))
      variables.append(v)
      transforms = next(in_transforms)
      assert isinstance(transforms, ir.ArrayAttr)
      ref_ty = cast(ir.MemRefType, value_site.value.type)
      tiling = _extract_smem_transforms_from_custom_transform_attrs(ref_ty, transforms)
      assignments[v] = tiling

  out_layouts = iter(op.out_layouts)
  for i, result in enumerate(op.results):
    if isinstance(result.type, ir.VectorType):
      v = cs.Variable(ValueSite(op, VariableType.RESULT, i))
      variables.append(v)
      assignments[v] = cs.RegisterLayout(
          layouts_lib.from_layout_attr(next(out_layouts))
      )
  return (
      cs.ConstraintSystem(assignments, constraints),
      {v: [v.key] for v in variables},
  )

