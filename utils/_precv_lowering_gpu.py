
def _precv_lowering_gpu(ctx, token, *, out_shape, axis_name, perm):
  full_perm, other_args = _pcollectives_lowering_common(
      ctx, axis_name=axis_name, perm=perm, op_name="precv"
  )
  out_type = mlir.aval_to_ir_type(ctx.module_context, out_shape)
  recv_op = hlo.RecvOp(
      [out_type, token.type],
      token,
      source_target_pairs=mlir.dense_int_elements(full_perm),
      **other_args,
  )
  axis_ctx = ctx.module_context.axis_context
  if not isinstance(axis_ctx, SPMDAxisContext):
    raise NotImplementedError("precv currently only supports manual sharding")

  # recv_op should return an array of [RankedTensorType, StableHlo.token]; we
  # only need the tensor.
  results = recv_op.results
  return [results[0]]

