
def _csr_matvec_gpu_lowering(ctx, data, indices, indptr, v, *, shape, transpose,
                             target_name_prefix):
  data_aval, indices_aval, _, v_aval = ctx.avals_in
  dtype = data_aval.dtype
  if dtype not in [np.float32, np.float64, np.complex64, np.complex128]:
    warnings.warn(f"csr_matvec cusparse/hipsparse lowering not available for {dtype=}. "
                  "Falling back to default implementation.", CuSparseEfficiencyWarning)
    return _csr_matvec_lowering(ctx, data, indices, indptr, v, shape=shape,
                                transpose=transpose)
  return _lowerings._csr_spmv_gpu_lowering(
      ctx, data, indices, indptr, v, shape=shape, transpose=transpose,
      target_name_prefix=target_name_prefix)

