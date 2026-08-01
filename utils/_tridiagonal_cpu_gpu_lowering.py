
def _tridiagonal_cpu_gpu_lowering(ctx, a, *, lower, target_name_prefix):
  a_aval, = ctx.avals_in
  arr_aval, d_aval, e_aval, taus_aval = ctx.avals_out
  batch_dims = a_aval.shape[:-2]
  if target_name_prefix == "cpu":
    real = a_aval.dtype == np.float32 or a_aval.dtype == np.float64
    prefix = "sy" if real else "he"
    target_name = lapack.prepare_lapack_call(f"{prefix}trd_ffi", a_aval.dtype)
    params = {"uplo": _matrix_uplo_attr(lower)}
  else:
    target_name = f"{target_name_prefix}solver_sytrd_ffi"
    params = {"lower": lower}
  info_aval = ShapedArray(batch_dims, np.int32)
  rule = _linalg_ffi_lowering(
      target_name, avals_out=(*ctx.avals_out, info_aval),
      operand_output_aliases={0: 0})
  arr, d, e, taus, info = rule(ctx, a, **params)
  zeros = mlir.full_like_aval(ctx, 0, info_aval)
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  arr = _replace_not_ok_with_nan(ctx, batch_dims, ok, arr, arr_aval)
  d = _replace_not_ok_with_nan(ctx, batch_dims, ok, d, d_aval)
  e = _replace_not_ok_with_nan(ctx, batch_dims, ok, e, e_aval)
  taus = _replace_not_ok_with_nan(ctx, batch_dims, ok, taus, taus_aval)
  return arr, d, e, taus

