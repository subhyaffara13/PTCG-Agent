
def _pack_dtype_eval_rule(ctx: block_spec.KernelEvalContext, *args, dtype):
  return dtype.pack_eval_rule(ctx, *args)

