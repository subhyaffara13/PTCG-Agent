
def _schur_cpu_lowering(ctx, operand, *, compute_schur_vectors, sort_eig_vals,
                        select_callable):
  del select_callable  # unused
  if sort_eig_vals:
    raise NotImplementedError(
        "The sort feature of LAPACK's gees routine is not implemented.")

  operand_aval, = ctx.avals_in
  batch_dims = operand_aval.shape[:-2]
  real = operand_aval.dtype == np.float32 or operand_aval.dtype == np.float64
  target_name = lapack.prepare_lapack_call("gees_ffi", operand_aval.dtype)

  info_aval = ShapedArray(batch_dims, np.dtype(np.int32))
  eigvals_aval = ShapedArray(operand_aval.shape[:-1], operand_aval.dtype)
  if real:
    avals_out = [operand_aval, operand_aval, eigvals_aval, eigvals_aval,
                 info_aval, info_aval]
  else:
    avals_out = [operand_aval, operand_aval, eigvals_aval, info_aval, info_aval]

  mode = (
      lapack.schur.ComputationMode.kComputeSchurVectors
      if compute_schur_vectors
      else lapack.schur.ComputationMode.kNoComputeSchurVectors
  )
  rule = _linalg_ffi_lowering(target_name, avals_out=avals_out,
                              operand_output_aliases={0: 0})
  schur_form, schur_vectors, *_, info = rule(
      ctx, operand, mode=_enum_attr(mode),
      sort=_enum_attr(lapack.schur.Sort.kNoSortEigenvalues))

  ok = mlir.compare_hlo(
      info, mlir.full_like_aval(ctx, 0, ShapedArray(batch_dims, np.dtype(np.int32))),
      "EQ", "SIGNED")

  schur_form = _replace_not_ok_with_nan(ctx, batch_dims, ok, schur_form,
                                        ctx.avals_out[0])
  output = [schur_form]
  if compute_schur_vectors:
    schur_vectors = _replace_not_ok_with_nan(ctx, batch_dims, ok, schur_vectors,
                                             ctx.avals_out[1])
    output.append(schur_vectors)

  return output

