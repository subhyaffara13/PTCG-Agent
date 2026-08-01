
def _geqp3_cpu_gpu_lowering(ctx, a, jpvt, *, use_magma, target_name_prefix):
  a_aval, _ = ctx.avals_in
  if target_name_prefix == "cpu":
    target_name = lapack.prepare_lapack_call("geqp3_ffi", a_aval.dtype)
    params = {}
  else:
    gpu_solver.initialize_hybrid_kernels()
    magma = config.gpu_use_magma.value
    target_name = f"{target_name_prefix}hybrid_geqp3"
    if use_magma is not None:
      magma = "on" if use_magma else "off"
    params = {"magma": magma}
  rule = _linalg_ffi_lowering(target_name, operand_output_aliases={0: 0, 1: 1})
  return rule(ctx, a, jpvt, **params)

