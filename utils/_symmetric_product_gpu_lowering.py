
def _symmetric_product_gpu_lowering(
    platform, ctx, a_tensor, c_tensor, alpha, beta):
  a_aval, c_aval = ctx.avals_in[:2]
  dtype = a_aval.dtype
  alpha_aval = beta_aval = ShapedArray((), dtype)

  alpha_array = mlir.full_like_aval(ctx, alpha, alpha_aval)
  beta_array = mlir.full_like_aval(ctx, beta, beta_aval)

  rule = ffi.ffi_lowering(f"{platform}solver_syrk_ffi",
                          operand_output_aliases={1: 0})
  ctx = ctx.replace(avals_in=[a_aval, c_aval, alpha_aval, beta_aval])
  return rule(ctx, a_tensor, c_tensor, alpha_array, beta_array, transpose=False)

