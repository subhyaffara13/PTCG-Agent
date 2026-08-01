
def _hessenberg_cpu_lowering(ctx, a):
  a_aval, = ctx.avals_in
  batch_dims = a_aval.shape[:-2]
  n = a_aval.shape[-1]
  if not core.is_constant_dim(n):
    raise ValueError("hessenberg requires the last dimension of a to be "
                     f"constant, got a.shape of {a.shape}.")
  target_name = lapack.prepare_lapack_call("gehrd_ffi", a_aval.dtype)
  avals_out = [*ctx.avals_out, ShapedArray(batch_dims, np.int32)]
  rule = _linalg_ffi_lowering(target_name, avals_out=avals_out,
                              operand_output_aliases={0: 0})
  a, taus, info = rule(ctx, a, low=np.int32(1), high=np.int32(n))
  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  return [
      _replace_not_ok_with_nan(ctx, batch_dims, ok, a, ctx.avals_out[0]),
      _replace_not_ok_with_nan(ctx, batch_dims, ok, taus, ctx.avals_out[1]),
  ]

