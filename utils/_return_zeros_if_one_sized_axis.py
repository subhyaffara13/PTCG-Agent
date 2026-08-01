
def _return_zeros_if_one_sized_axis(
  ctx: roofline.RooflineRuleContext, axes: tuple[str, ...]
) -> roofline.RooflineResult | None:
  assert ctx.mesh
  axes_size = np.prod([ctx.mesh.shape[axis] for axis in axes])
  if axes_size > 1:
    return None
  return roofline.RooflineResult(
    ici_bytes={axis: 0 for axis in axes},
    ici_latency={axis: 0 for axis in axes},
  )

