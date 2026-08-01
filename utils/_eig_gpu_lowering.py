
def _eig_gpu_lowering(ctx, operand, *,
                      compute_left_eigenvectors, compute_right_eigenvectors,
                      enable_eigvec_derivs, implementation, target_name_prefix):
  del enable_eigvec_derivs
  operand_aval, = ctx.avals_in
  batch_dims = operand_aval.shape[:-2]
  n, m = operand_aval.shape[-2:]
  assert n == m

  dtype = operand_aval.dtype
  complex_dtype = np.result_type(dtype, 1j)
  if dtype in (np.float32, np.float64):
    is_real = True
  elif dtype in (np.complex64, np.complex128):
    is_real = False
  else:
    raise ValueError(f"Unsupported dtype: {dtype}")

  have_cusolver_geev = (
      target_name_prefix == "cu"
      and cuda_versions
      and cuda_versions.cusolver_get_version() >= 11701
  )

  if (
      implementation is None and have_cusolver_geev
      and not compute_left_eigenvectors
  ) or implementation == EigImplementation.CUSOLVER:
    if not have_cusolver_geev:
      raise RuntimeError(
          "Nonsymmetric eigendecomposition requires cusolver 11.7.1 or newer"
      )
    if compute_left_eigenvectors:
      raise NotImplementedError(
          "Left eigenvectors are not supported by cusolver")
    target_name = f"{target_name_prefix}solver_geev_ffi"
    avals_out = [
        ShapedArray(batch_dims + (n, n), dtype),
        ShapedArray(batch_dims + (n,), complex_dtype),
        ShapedArray(batch_dims + (n, n), dtype),
        ShapedArray(batch_dims + (n, n), dtype),
        ShapedArray(batch_dims, np.int32),
    ]

    rule = _linalg_ffi_lowering(target_name, avals_out=avals_out)
    _, w, vl, vr, info = rule(ctx, operand, left=compute_left_eigenvectors,
                              right=compute_right_eigenvectors)
    if is_real:
      unpack = mlir.lower_fun(_unpack_conjugate_pairs, multiple_results=False)
      if compute_left_eigenvectors:
        sub_ctx = ctx.replace(
            primitive=None,
            avals_in=[
                ShapedArray(batch_dims + (n,), complex_dtype),
                ShapedArray(batch_dims + (n, n), dtype),
            ],
            avals_out=[ShapedArray(batch_dims + (n, n), complex_dtype)],
        )
        vl, = unpack(sub_ctx, w, vl)
      if compute_right_eigenvectors:
        sub_ctx = ctx.replace(
            primitive=None,
            avals_in=[
                ShapedArray(batch_dims + (n,), complex_dtype),
                ShapedArray(batch_dims + (n, n), dtype),
            ],
            avals_out=[ShapedArray(batch_dims + (n, n), complex_dtype)],
        )
        vr, = unpack(sub_ctx, w, vr)
  else:
    magma = config.gpu_use_magma.value
    if implementation is not None:
      magma = "on" if implementation == EigImplementation.MAGMA else "off"
    gpu_solver.initialize_hybrid_kernels()
    if is_real:
      target_name = f"{target_name_prefix}hybrid_eig_real"
      complex_dtype = np.complex64 if dtype == np.float32 else np.complex128
    else:
      target_name = f"{target_name_prefix}hybrid_eig_comp"
      assert dtype == np.complex64 or dtype == np.complex128
      complex_dtype = dtype

    avals_out = [
        ShapedArray(batch_dims + (n,), dtype),
        ShapedArray(batch_dims + (n, n), complex_dtype),
        ShapedArray(batch_dims + (n, n), complex_dtype),
        ShapedArray(batch_dims, np.int32),
    ]
    if is_real:
      avals_out = [ShapedArray(batch_dims + (n,), dtype)] + avals_out
    rule = _linalg_ffi_lowering(target_name, avals_out=avals_out)
    *w, vl, vr, info = rule(ctx, operand, magma=magma,
                            left=compute_left_eigenvectors,
                            right=compute_right_eigenvectors)
    if is_real:
      assert len(w) == 2
      w = hlo.complex(*w)
    else:
      assert len(w) == 1
      w = w[0]
  zeros = mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.int32))
  ok = mlir.compare_hlo(info, zeros, "EQ", "SIGNED")
  w_aval = ShapedArray(batch_dims + (n,), complex_dtype)
  w = _replace_not_ok_with_nan(ctx, batch_dims, ok, w, w_aval)
  output = [w]
  if compute_left_eigenvectors:
    vl_aval = ShapedArray(batch_dims + (n, n), complex_dtype)
    vl = _replace_not_ok_with_nan(ctx, batch_dims, ok, vl, vl_aval)
    output.append(vl)
  if compute_right_eigenvectors:
    vr_aval = ShapedArray(batch_dims + (n, n), complex_dtype)
    vr = _replace_not_ok_with_nan(ctx, batch_dims, ok, vr, vr_aval)
    output.append(vr)
  return output

