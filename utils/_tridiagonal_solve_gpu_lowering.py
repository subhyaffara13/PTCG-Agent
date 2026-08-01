
def _tridiagonal_solve_gpu_lowering(ctx, dl, d, du, b, *, target_name_prefix,
                                    perturb_singular):
  m = ctx.avals_in[1].shape[-1]
  if perturb_singular:
    b_aval = ctx.avals_in[-1]
    target_name = f"{target_name_prefix}_tridiagonal_solve_perturbed"
    rule = _linalg_ffi_lowering(target_name, avals_out=[b_aval])
    return rule(ctx, dl, d, du, b)

  # The cusolver implementation requires m >= 3.
  if m <= 2:
    return mlir.lower_fun(_tridiagonal_solve_jax, multiple_results=False)(
        ctx, dl, d, du, b, perturb_singular=perturb_singular)
  target_name = f"{target_name_prefix}sparse_gtsv2_ffi"
  rule = _linalg_ffi_lowering(target_name, operand_output_aliases={3: 0})
  return rule(ctx, dl, d, du, b)

