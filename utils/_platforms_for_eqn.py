
def _platforms_for_eqn(ctx: LoweringRuleContext) -> tuple[str, ...]:
  """The lowering platforms for the current eqn"""
  return tuple(_platforms_for_eqn_ctx(ctx.jaxpr_eqn_ctx) or
               ctx.platforms or ctx.module_context.platforms)

