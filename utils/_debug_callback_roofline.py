
def _debug_callback_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    **kw,
) -> roofline.RooflineResult:
  avals_in = ctx.avals_in
  # `debug_callback` does not return values to the JAX program, so only input
  # HBM bytes are considered.
  hbm_bytes = roofline.RooflineShape.total_bytes(avals_in)
  # We don't have access to the `callback_func`, so we assume it contributes 0
  # flops.
  return roofline.RooflineResult(unfused_hbm_bytes=hbm_bytes)

