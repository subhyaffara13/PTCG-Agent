
def _lu_cpu_gpu_lowering(ctx, operand, *, target_name_prefix: str):
  operand_aval, = ctx.avals_in
  out_aval, pivot_aval, perm_aval = ctx.avals_out
  batch_dims = operand_aval.shape[:-2]
  info_aval = ShapedArray(batch_dims, np.dtype(np.int32))
  m = operand_aval.shape[-2]

  if target_name_prefix == "cpu":
    target_name = lapack.prepare_lapack_call("getrf_ffi", operand_aval.dtype)
  else:
    target_name = f"{target_name_prefix}solver_getrf_ffi"
  rule = _linalg_ffi_lowering(target_name,
                              avals_out=[out_aval, pivot_aval, info_aval],
                              operand_output_aliases={0: 0})
  lu, pivot, info = rule(ctx, operand)

  # Subtract 1 from the pivot to get 0-based indices.
  pivot = hlo.subtract(pivot, mlir.full_like_aval(ctx, 1, pivot_aval))
  ok = mlir.compare_hlo(info, mlir.full_like_aval(ctx, 0, info_aval),
      "GE", "SIGNED")
  lu = _replace_not_ok_with_nan(ctx, batch_dims, ok, lu, out_aval)
  sub_ctx = ctx.replace(primitive=None, avals_in=[pivot_aval],
                        avals_out=[perm_aval])
  perm_fn = mlir.lower_fun(lambda x: lu_pivots_to_permutation(x, m),
                           multiple_results=False)
  perm, = perm_fn(sub_ctx, pivot)
  return [lu, pivot, perm]

