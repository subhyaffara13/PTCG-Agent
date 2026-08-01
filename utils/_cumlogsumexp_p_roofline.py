
def _cumlogsumexp_p_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    axis: int,
    **kw,
) -> roofline.RooflineResult:
  (x,) = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])
  return roofline.RooflineResult(
      # Similar to `cum{max, min, prod, sum}`, `cumlogsumexp` only calculates
      # values for one axis. But for `x.shape[axis] = S`, it computes (for a
      # naive implementation):
      #   S `exp` ops.
      #   S-1 `add` ops.
      #   1 log op.
      # Thus, the total number of flops is 2 * S.
      unfused_flops=x.shape[axis] * 2,
      unfused_hbm_bytes=(
          x.dtype.itemsize * x.size + out.dtype.itemsize * out.size
      ),
  )

