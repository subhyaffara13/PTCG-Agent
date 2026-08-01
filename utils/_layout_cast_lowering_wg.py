
def _layout_cast_lowering_wg(
    ctx: LoweringRuleContext, x, *, new_layout
):
  layout = new_layout.to_mgpu()
  if ctx.avals_in[0].ndim == 0:  # scalar case
    if layout != mgpu.WGSplatFragLayout():
      raise ValueError(
          "Only plgpu.Layout.WG_SPLAT is supported for scalar values."
      )
    return x
  return mgpu.dialect.layout_cast(x, mgpu.to_layout_attr(layout))

