
def _geqrf_cpu_gpu_lowering(ctx, a, *, target_name_prefix: str):
  operand_aval, = ctx.avals_in
  if target_name_prefix == "cpu":
    target_name = lapack.prepare_lapack_call("geqrf_ffi", operand_aval.dtype)
  else:
    target_name = f"{target_name_prefix}solver_geqrf_ffi"
  rule = _linalg_ffi_lowering(target_name, operand_output_aliases={0: 0})
  return rule(ctx, a)

