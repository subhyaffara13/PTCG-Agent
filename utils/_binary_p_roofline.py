
def _binary_p_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    **kw,
) -> roofline.RooflineResult:
  lhs, rhs = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  broadcasted_shape = [
      max(l, r) for l, r in it.zip_longest(lhs.shape, rhs.shape, fillvalue=1)
  ]
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])
  return roofline.RooflineResult(
      unfused_flops=int(np.prod(broadcasted_shape)),
      unfused_hbm_bytes=(
          lhs.dtype.itemsize * lhs.size
          + rhs.dtype.itemsize * rhs.size
          + out.dtype.itemsize * out.size
      ),
  )

