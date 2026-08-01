
def core_map_lowering_rule(ctx: mlir.LoweringRuleContext,
    *args,
    jaxpr,
    **kwargs
  ):
  del ctx, args, kwargs
  raise ValueError(
      "Attempted to lower core_map without discharging. This can happen if "
      "the core_map body does not modify any Refs or have other observable "
      f"side-effects.\n Jaxpr of the body: {jaxpr}")

