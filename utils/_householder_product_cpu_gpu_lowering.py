
def _householder_product_cpu_gpu_lowering(ctx, a, taus, *,
                                          target_name_prefix: str):
  a_aval, _ = ctx.avals_in
  if target_name_prefix == "cpu":
    dtype = a_aval.dtype
    prefix = "un" if dtypes.issubdtype(dtype, np.complexfloating) else "or"
    target_name = lapack.prepare_lapack_call(f"{prefix}gqr_ffi", dtype)
  else:
    target_name = f"{target_name_prefix}solver_orgqr_ffi"
  rule = _linalg_ffi_lowering(target_name, operand_output_aliases={0: 0})
  return rule(ctx, a, taus)

