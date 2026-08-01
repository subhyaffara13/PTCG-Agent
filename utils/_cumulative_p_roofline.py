
def _cumulative_p_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    axis: int,
    **kw,
) -> roofline.RooflineResult:
  (x,) = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])
  return roofline.RooflineResult(
      # `cum{max, min, prod, sum}` only calculate values for one axis.
      unfused_flops=x.shape[axis],
      unfused_hbm_bytes=(
          x.dtype.itemsize * x.size + out.dtype.itemsize * out.size
      ),
  )

