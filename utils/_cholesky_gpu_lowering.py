
def _cholesky_gpu_lowering(ctx, operand, *, target_name_prefix):
  operand_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  info_aval = ShapedArray(batch_dims, np.int32)
  rule = _linalg_ffi_lowering(f"{target_name_prefix}solver_potrf_ffi",
                              avals_out=[operand_aval, info_aval],
                              operand_output_aliases={0: 0})
  result, info = rule(ctx, operand, lower=True)
  ok = mlir.compare_hlo(info, mlir.full_like_aval(ctx, 0, info_aval), "EQ",
                        "SIGNED")
  return [_replace_not_ok_with_nan(ctx, batch_dims, ok, result, out_aval)]

