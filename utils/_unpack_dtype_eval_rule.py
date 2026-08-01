
def _unpack_dtype_eval_rule(ctx: block_spec.KernelEvalContext, *args):
  assert ctx.avals_in is not None
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  assert isinstance(aval_in.dtype, FusionDType), aval_in.dtype
  return aval_in.dtype.unpack_eval_rule(ctx, *args)  # pyrefly: ignore[missing-attribute]

