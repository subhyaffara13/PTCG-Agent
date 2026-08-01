
def _psum2_roofline(
  ctx: roofline.RooflineRuleContext,
  *args,
  axes: tuple[str, ...],
  **kw,
) -> roofline.RooflineResult:
  ring_roofline = _ring_collective_roofline(ctx, *args, axes=axes, **kw)

  def double_dict(d: dict[str, int]) -> dict[str, int]:
    return {k: v * 2 for k, v in d.items()}

  return roofline.RooflineResult(
    ici_bytes=double_dict(ring_roofline.ici_bytes),
    ici_latency=double_dict(ring_roofline.ici_latency),
  )

