
def _dot_general_roofline(
  ctx: roofline.RooflineRuleContext,
  *args,
  dimension_numbers: lax.DotDimensionNumbers,
  **kw,
) -> roofline.RooflineResult:
  lhs, rhs = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])
  (lhs_contract, _), (lhs_batch, _) = dimension_numbers

  flops = (
    _FMA_FLOPS_FACTOR
    * lhs.size
    * rhs.size
    / np.prod([lhs.shape[i] for i in lhs_contract])
    / np.prod([lhs.shape[i] for i in lhs_batch])
  )

  hbm_bytes = 0
  if not ctx.pin_lhs_in_vmem:
    hbm_bytes += lhs.bytes
    hbm_bytes += out.bytes
  if not ctx.pin_rhs_in_vmem:
    hbm_bytes += rhs.bytes

  return roofline.RooflineResult(
      flops=int(flops),
      unfused_flops=int(flops),
      hbm_bytes=hbm_bytes,
      unfused_hbm_bytes=hbm_bytes,
  )

