
def _get_override_lowering_rule(
    ctx: ModuleContext, primitive: core.Primitive
) -> LoweringRule | None:
  if ctx.lowering_parameters.override_lowering_rules is None:
    return None
  for p, rule in ctx.lowering_parameters.override_lowering_rules:
    if primitive is p:
      return rule
  return None

