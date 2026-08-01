
def _eigh_cpu_gpu_lowering(
    ctx, operand, *, lower, sort_eigenvalues, subset_by_index, algorithm,
    target_name_prefix: str
):
  del sort_eigenvalues  # The CPU/GPU implementations always sort.
  operand_aval, = ctx.avals_in
  v_aval, w_aval = ctx.avals_out
  n = operand_aval.shape[-1]
  if not (subset_by_index is None or subset_by_index == (0, n)):
    raise NotImplementedError("subset_by_index not supported on CPU and GPU")
  batch_dims = operand_aval.shape[:-2]

  if algorithm == EighImplementation.QDWH:
    raise NotImplementedError("QDWH implementation is only supported on TPU")
  if algorithm == EighImplementation.JACOBI and target_name_prefix == "cpu":
    raise NotImplementedError("Jacobi implementation is not supported on CPU")

  if target_name_prefix == "cpu":
    dtype = operand_aval.dtype
    prefix = "he" if dtypes.issubdtype(dtype, np.complexfloating) else "sy"
    target_name = lapack.prepare_lapack_call(f"{prefix}evd_ffi",
                                             operand_aval.dtype)
    kwargs = {
      "mode": np.uint8(ord("V")),
      "uplo": np.uint8(ord("L" if lower else "U")),
    }
  else:
    target_name = f"{target_name_prefix}solver_syevd_ffi"
    # Use Jacobi (algorithm=2) if requested, otherwise use QR (algorithm=1)
    if algorithm is None:
      algo_int = 0
    else:
      algo_int = 2 if algorithm == EighImplementation.JACOBI else 1
    kwargs = {"lower": lower, "algorithm": np.uint8(algo_int)}

  info_aval = ShapedArray(batch_dims, np.int32)
  avals_out = [v_aval, w_aval, info_aval]
  rule = _linalg_ffi_lowering(target_name, avals_out=avals_out,
                              operand_output_aliases={0: 0})
  v, w, info = rule(ctx, operand, **kwargs)

  zeros = mlir.full_like_aval(ctx, 0, info_aval)
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  v = _replace_not_ok_with_nan(ctx, batch_dims, ok, v, v_aval)
  w = _replace_not_ok_with_nan(ctx, batch_dims, ok, w, w_aval)
  return [v, w]

