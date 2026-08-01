
def _callback_with_output_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    **kw,
) -> roofline.RooflineResult:
  avals_in = ctx.avals_in
  avals_out = ctx.avals_out
  # HBM bytes for transferring inputs to host and results back to device.
  hbm_bytes = roofline.RooflineShape.total_bytes(
      avals_in
  ) + roofline.RooflineShape.total_bytes(avals_out)
  # We don't have access to the `callback_func`, so we assume it contributes 0
  # flops.
  return roofline.RooflineResult(unfused_hbm_bytes=hbm_bytes)

