
def _unpack_dtype_push_rule(
    ctx: block_spec.PushRuleContext,
    block_spec: pallas_core.BlockSpec,
):
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  assert isinstance(aval_in.dtype, FusionDType), aval_in.dtype
  return aval_in.dtype.unpack_push_block_spec(aval_in, block_spec)

