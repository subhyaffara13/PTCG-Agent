
def _psend_lowering_gpu(ctx, x, *, axis_name, perm):
  if ("cuda" not in ctx.module_context.platforms and
      "rocm" not in ctx.module_context.platforms):
    raise NotImplementedError("psend is currently only implemented on GPUs")

  full_perm, other_args = _pcollectives_lowering_common(
      ctx, axis_name=axis_name, perm=perm, op_name="psend"
  )
  token = hlo.create_token()
  send_op = hlo.SendOp(
      [x],
      token,
      source_target_pairs=mlir.dense_int_elements(full_perm),
      **other_args,
  )
  axis_ctx = ctx.module_context.axis_context
  if not isinstance(axis_ctx, SPMDAxisContext):
    raise NotImplementedError("psend currently only supports manual sharding")

  return send_op.results

