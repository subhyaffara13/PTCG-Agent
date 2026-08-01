
def _get_token_sharding(
    ctx: mlir.LoweringRuleContext, mesh
  ) -> sharding_impls.SdyArray:
  ns = _make_scoped_manual_sharding(ctx, mesh, P())
  return ns._to_sdy_sharding(0)

