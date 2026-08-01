
def _tridiagonal_solve_cpu_lowering(ctx, dl, d, du, b, *, perturb_singular):
  b_aval = ctx.avals_in[-1]
  batch_dims = b_aval.shape[:-2]

  if perturb_singular:
    target_name = "tridiagonal_solve_perturbed_ffi"
    rule = _linalg_ffi_lowering(target_name, avals_out=[b_aval])
    return rule(ctx, dl, d, du, b)

  target_name = lapack.prepare_lapack_call("gtsv_ffi", b_aval.dtype)
  info_aval = ShapedArray(batch_dims, np.int32)
  rule = _linalg_ffi_lowering(target_name,
                              avals_out=[*ctx.avals_in, info_aval],
                              operand_output_aliases={0: 0, 1: 1, 2: 2, 3: 3})
  *_, b_out, info = rule(ctx, dl, d, du, b)
  zeros = mlir.full_like_aval(ctx, 0, info_aval)
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  return [_replace_not_ok_with_nan(ctx, batch_dims, ok, b_out, b_aval)]

