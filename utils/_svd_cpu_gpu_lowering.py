
def _svd_cpu_gpu_lowering(
    ctx,
    operand,
    *,
    full_matrices,
    compute_uv,
    subset_by_index,
    target_name_prefix: str,
    algorithm=None,
):
  operand_aval, = ctx.avals_in
  s_aval = ctx.avals_out[0]
  m, n = operand_aval.shape[-2:]
  batch_dims = operand_aval.shape[:-2]

  if not (subset_by_index is None or subset_by_index == (0, min(m, n))):
    raise NotImplementedError("subset_by_index not implemented for CPU and GPU")

  if m == 0 or n == 0:
    return mlir.lower_fun(_empty_svd, multiple_results=True)(
        ctx,
        operand,
        full_matrices=full_matrices,
        compute_uv=compute_uv,
    )
  if target_name_prefix == "cpu":
    if algorithm is None or algorithm == SvdAlgorithm.DEFAULT:
      target_name = lapack.prepare_lapack_call("gesdd_ffi", operand_aval.dtype)
    elif algorithm == SvdAlgorithm.QR:
      target_name = lapack.prepare_lapack_call("gesvd_ffi", operand_aval.dtype)
    elif algorithm == SvdAlgorithm.DIVIDE_AND_CONQUER:
      target_name = lapack.prepare_lapack_call("gesdd_ffi", operand_aval.dtype)
    else:
      raise NotImplementedError(
          "The SVD Jacobi and Polar algorithms are not implemented on CPU.")
    mode = _svd_computation_attr(compute_uv, full_matrices)
    info_aval = ShapedArray(batch_dims, np.dtype(np.int32))
    if compute_uv:
      s_aval, u_aval, vt_aval = ctx.avals_out
    else:
      s_aval, = ctx.avals_out
      # TODO(danfm): It should be possible to skip instantiating these arrays
      # when they are not used.
      u_aval = ShapedArray((*batch_dims, m,
                            m if full_matrices else core.min_dim(m, n)),
                           operand_aval.dtype)
      vt_aval = ShapedArray((*batch_dims,
                             n if full_matrices else core.min_dim(m, n), n),
                            operand_aval.dtype)
    avals_out = [operand_aval, s_aval, u_aval, vt_aval, info_aval]
    rule = _linalg_ffi_lowering(target_name, avals_out=avals_out,
                                operand_output_aliases={0: 0})
    _, s, u, vt, info = rule(ctx, operand, mode=mode)
  else:
    s, u, vt, info = _svd_gpu_sub_lowering(ctx, operand,
                                           full_matrices=full_matrices,
                                           compute_uv=compute_uv,
                                           target_name_prefix=target_name_prefix,
                                           algorithm=algorithm)

  zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32)))
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  s = _replace_not_ok_with_nan(ctx, batch_dims, ok, s, s_aval)
  result = [s]
  if compute_uv:
    u_aval, vt_aval = ctx.avals_out[1:]
    u = _replace_not_ok_with_nan(ctx, batch_dims, ok, u, u_aval)
    vt = _replace_not_ok_with_nan(ctx, batch_dims, ok, vt, vt_aval)
    result += [u, vt]

  return result

