
def _gather_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    mode: slicing.GatherScatterMode,
    **kw,
) -> roofline.RooflineResult:
  _, indices = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])

  # Gather doesn't read the whole input buffer, it's equivalent to a copy the
  # size of the output shape and a read of the gather indices.
  unfused_hbm_bytes = (
      out.dtype.itemsize * out.size * 2 + indices.dtype.itemsize * indices.size
  )

  return roofline.RooflineResult(
      unfused_flops=_calculate_gather_flops(mode, indices.size, out.size),
      unfused_hbm_bytes=unfused_hbm_bytes,
  )

