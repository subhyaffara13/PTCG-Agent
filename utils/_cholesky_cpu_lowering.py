
def _cholesky_cpu_lowering(ctx, operand):
  operand_aval, = ctx.avals_in
  out_aval, = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  target_name = lapack.prepare_lapack_call("potrf_ffi", operand_aval.dtype)
  info_aval = ShapedArray(batch_dims, np.int32)
  rule = _linalg_ffi_lowering(target_name, avals_out=[operand_aval, info_aval],
                              operand_output_aliases={0: 0})
  result, info = rule(ctx, operand, uplo=_matrix_uplo_attr(True))
  ok = mlir.compare_hlo(info, mlir.full_like_aval(ctx, 0, info_aval), "EQ",
                        "SIGNED")
  return [_replace_not_ok_with_nan(ctx, batch_dims, ok, result, out_aval)]

