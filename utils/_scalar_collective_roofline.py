
def _scalar_collective_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    axes: tuple[str, ...],
    **kw,
) -> roofline.RooflineResult:
  shapes = [roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in]
  ctx = replace(ctx, avals_in=[core.ShapedArray((1,), shape.dtype) for shape in shapes])
  return _ring_collective_roofline(ctx, *args, axes=axes, is_reduce=False, **kw)

