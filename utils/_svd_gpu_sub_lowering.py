from typing import Any

def _svd_gpu_sub_lowering(ctx, operand, *, full_matrices, compute_uv,
                          target_name_prefix, algorithm):
  operand_aval, = ctx.avals_in
  if compute_uv:
    s_aval, u_aval, vt_aval = ctx.avals_out
  else:
    s_aval, = ctx.avals_out
    u_aval = vt_aval = ShapedArray((), operand_aval.dtype)
  batch_dims = operand_aval.shape[:-2]
  info_aval = ShapedArray(batch_dims, np.dtype(np.int32))
  nb = len(batch_dims)
  m, n = operand_aval.shape[-2:]
  k = core.min_dim(m, n)

  # DEFAULT and explicit algorithms: _resolve_gpu_svd_implementation. CUDA
  # Jacobi for m,n <= 1024 when dimensions are concrete; otherwise GESVD. See
  # https://developer.download.nvidia.com/video/gputechconf/gtc/2019/presentation/s9226-fast-singular-value-decomposition-on-gpus-v2.pdf
  # slide 5.
  impl = _resolve_gpu_svd_implementation(
      ctx, target_name_prefix, algorithm, m, n)

  column_major = True
  econ = not full_matrices
  transposed = False
  kwargs: dict[str, Any] = {}

  if impl == _GpuSvdImpl.JACOBI:
    target_name = f"{target_name_prefix}solver_gesvdj_ffi"
    # gesvdjbatched: no "econ" mode; batched path worthwhile up to 32x32.
    try:
      econ = not full_matrices and m > 32 and n > 32
    except core.InconclusiveDimensionOperation:
      econ = False
  elif impl == _GpuSvdImpl.POLAR:
    target_name = f"{target_name_prefix}solver_gesvdp_ffi"
  elif impl == _GpuSvdImpl.GESDD:
    target_name = f"{target_name_prefix}solver_gesdd_ffi"
    # The gesdd FFI handler accepts the same attribute schema as gesvd:
    # (full_matrices, compute_uv, transposed). For gesdd this is always false.
    kwargs = {"transposed": False}
  elif impl in (_GpuSvdImpl.QR_GESVD, _GpuSvdImpl.GESVD):
    target_name = f"{target_name_prefix}solver_gesvd_ffi"
    transposed = m < n
    kwargs = {"transposed": transposed}
    if transposed:
      column_major = False
  else:
    raise AssertionError(impl)

  if impl in (_GpuSvdImpl.JACOBI, _GpuSvdImpl.POLAR):
    # When using the Jacobi or polar algorithms, the U and V matrices must
    # always be allocated even if compute_uv is False.
    u_aval = ShapedArray((*batch_dims, m, k if econ else m), u_aval.dtype)
    v_aval = ShapedArray((*batch_dims, n, k if econ else n), vt_aval.dtype)
    avals_out = [operand_aval, s_aval, u_aval, v_aval, info_aval]
  elif transposed:
    avals_out = [operand_aval, s_aval, vt_aval, u_aval, info_aval]
  else:
    avals_out = [operand_aval, s_aval, u_aval, vt_aval, info_aval]

  rule = _linalg_ffi_lowering(target_name, avals_out=avals_out,
                              operand_output_aliases={0: 0},
                              column_major=column_major)
  _, s, u, vt, info = rule(ctx, operand, full_matrices=not econ,
                           compute_uv=compute_uv, **kwargs)
  if impl in (_GpuSvdImpl.JACOBI, _GpuSvdImpl.POLAR) and compute_uv:
    vt = hlo.transpose(
        vt,
        mlir.dense_int_array(tuple(range(nb)) + (nb + 1, nb)))
    if np.issubdtype(operand_aval.dtype, np.complexfloating):
      vt = hlo.complex(hlo.real(vt), hlo.negate(hlo.imag(vt)))
    if not full_matrices and not econ:
      nd = len(operand_aval.shape)
      u = mlir.slice_op(ctx, u, ctx.avals_out[1],
                        start_indices=np.zeros([nd], np.int64),
                        limit_indices=batch_dims + (m, k),
                        strides=np.ones([nd], np.int64))
      vt = mlir.slice_op(ctx, vt, ctx.avals_out[2],
                         start_indices=np.zeros([nd], np.int64),
                         limit_indices=batch_dims + (k, n),
                         strides=np.ones([nd], np.int64))
  if transposed:
    return s, vt, u, info
  else:
    return s, u, vt, info

