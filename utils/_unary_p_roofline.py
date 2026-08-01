
def _unary_p_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    **kw,
) -> roofline.RooflineResult:
  (x,) = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])
  return roofline.RooflineResult(
      unfused_flops=x.size,
      unfused_hbm_bytes=(
          x.dtype.itemsize * x.size + out.dtype.itemsize * out.size
      ),
  )

