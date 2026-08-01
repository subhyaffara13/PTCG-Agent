
def _cholesky_update_gpu_lowering_rule(target_name_prefix, ctx, r_matrix,
                                       w_vector):
  rule = ffi.ffi_lowering(f"{target_name_prefix}_cholesky_update_ffi",
                          operand_output_aliases={0: 0, 1: 1})
  sub_ctx = ctx.replace(avals_out=ctx.avals_in)
  return rule(sub_ctx, r_matrix, w_vector)[:1]

