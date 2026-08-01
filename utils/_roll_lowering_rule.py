
def _roll_lowering_rule(
    ctx: LoweringRuleContext, x, shift, *, axis, stride, stride_axis
):
  return tpu.dynamic_rotate(
      x,
      shift,
      axis,
      stride=stride,
      stride_dimension=stride_axis,
  )


def _roll_lowering_rule(
    ctx: mlir.LoweringRuleContext, x, shift, *, axis, stride, stride_axis
):
  def _roll(x, shift):
    if stride is None:
      return jnp.roll(x, shift, axis)
    outputs = [
        jnp.roll(xs, shift + i * stride, axis)
        for i, xs in enumerate(jnp.split(x, x.shape[stride_axis], stride_axis))
    ]
    return jnp.concatenate(outputs, stride_axis)

  return mlir.lower_fun(_roll, multiple_results=False)(ctx, x, shift)

