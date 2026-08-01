
def _conv_general_dilated_roofline(
    ctx: roofline.RooflineRuleContext,
    *args,
    window_strides: Sequence[int],
    padding: Sequence[tuple[int, int]],
    lhs_dilation: Sequence[int],
    rhs_dilation: Sequence[int],
    dimension_numbers: convolution.ConvGeneralDilatedDimensionNumbers,
    batch_group_count: int,
    **kw,
) -> roofline.RooflineResult:
  """Roofline for Jax's conv_general_dilated primitive.

  See `jax.lax.conv_general_dilated` for details on the arguments.
  """
  lhs, rhs = (roofline.RooflineShape.from_aval(aval) for aval in ctx.avals_in)
  out = roofline.RooflineShape.from_aval(ctx.avals_out[0])

  return roofline.RooflineResult(
      unfused_flops=_calculate_conv_flops(
          lhs,
          rhs,
          out,
          window_strides,
          padding,
          lhs_dilation,
          rhs_dilation,
          dimension_numbers,
          batch_group_count,
      ),
      unfused_hbm_bytes=(
          lhs.dtype.itemsize * lhs.size
          + rhs.dtype.itemsize * rhs.size
          + out.dtype.itemsize * out.size
      ),
  )

