
def _eig_cpu_lowering(ctx, operand, *, compute_left_eigenvectors,
                      compute_right_eigenvectors, enable_eigvec_derivs,
                      implementation):
  del enable_eigvec_derivs
  if implementation and implementation != EigImplementation.LAPACK:
    raise ValueError("Only the lapack implementation is supported on CPU.")
  operand_aval, = ctx.avals_in
  out_aval = ctx.avals_out[0]
  batch_dims = operand_aval.shape[:-2]
  real = operand_aval.dtype == np.float32 or operand_aval.dtype == np.float64
  eigvals_aval = ShapedArray(operand_aval.shape[:-1], operand_aval.dtype)
  eigvecs_aval = ShapedArray(operand_aval.shape,
                              dtypes.to_complex_dtype(operand_aval.dtype))
  info_aval = ShapedArray(batch_dims, np.int32)
  avals_out = [eigvals_aval, eigvecs_aval, eigvecs_aval, info_aval]
  if real:
    avals_out = [eigvals_aval, *avals_out]
  target_name = lapack.prepare_lapack_call("geev_ffi", operand_aval.dtype)
  rule = _linalg_ffi_lowering(target_name, avals_out=avals_out)
  *w, vl, vr, info = rule(ctx, operand,
                          compute_left=_eig_compute_attr(compute_left_eigenvectors),
                          compute_right=_eig_compute_attr(compute_right_eigenvectors))
  w = hlo.complex(w[0], w[1]) if real else w[0]

  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")
  w = _replace_not_ok_with_nan(ctx, batch_dims, ok, w, out_aval)
  output = [w]
  if compute_left_eigenvectors:
    aval = ctx.avals_out[len(output)]
    vl = _replace_not_ok_with_nan(ctx, batch_dims, ok, vl, aval)
    output.append(vl)
  if compute_right_eigenvectors:
    aval = ctx.avals_out[len(output)]
    vr = _replace_not_ok_with_nan(ctx, batch_dims, ok, vr, aval)
    output.append(vr)
  return output

