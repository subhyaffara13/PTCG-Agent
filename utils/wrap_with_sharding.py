
def wrap_with_sharding(
    ctx: mlir.LoweringRuleContext,
    x: ir.Value,
    x_aval: core.AbstractValue,
    x_sharding: sharding_impls.NamedSharding | sharding_impls.GSPMDSharding | HloSharding | None,
    use_shardy: bool,
) -> ir.Value:
  if x_sharding is None:
    return x
  if use_shardy:
    x_sharding = x_sharding._to_sdy_sharding(x_aval.ndim)  # pyrefly: ignore[missing-attribute]
  else:
    x_sharding = x_sharding.to_proto()  # pyrefly: ignore[missing-attribute]
  return mlir.wrap_with_sharding_op(ctx, x, x_aval, x_sharding,
                                    allow_shardy_lowering=use_shardy)

