
def _threefry2x32_gpu_lowering_rule(ctx, k1, k2, x1, x2, *, target_name_prefix):
  if not config.threefry_gpu_kernel_lowering.value:  # back to default lowering
    return _threefry2x32_lowering_rule(ctx, k1, k2, x1, x2)

  aval_out, aval_out_2 = ctx.avals_out
  assert aval_out == aval_out_2
  k1_aval, k2_aval, x1_aval, x2_aval = ctx.avals_in
  rank = len(aval_out.shape)
  if 0 in aval_out.shape:
    zeros = mlir.full_like_aval(ctx, 0, aval_out)
    return [zeros, zeros]
  def _broadcast(x, aval):
    return mlir.broadcast_in_dim(ctx, x, aval_out,
                                 broadcast_dimensions=range(rank - len(aval.shape), rank))

  sub_ctx = ctx.replace(avals_in=(aval_out,) * 4)
  rule = ffi.ffi_lowering(
      f"{target_name_prefix}_threefry2x32_ffi")
  return rule(sub_ctx, _broadcast(k1, k1_aval), _broadcast(k2, k2_aval),
              _broadcast(x1, x1_aval), _broadcast(x2, x2_aval))

