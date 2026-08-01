
def _coo_fromdense_gpu_lowering(ctx, mat, *, nse, index_dtype, target_name_prefix):
  dtype = ctx.avals_in[0].dtype
  if not (np.issubdtype(dtype, np.floating) or np.issubdtype(dtype, np.complexfloating)):
    warnings.warn(f"coo_fromdense cusparse/hipsparse lowering not available for {dtype=}. "
                  "Falling back to default implementation.", CuSparseEfficiencyWarning)
    return _coo_fromdense_lowering(ctx, mat, nse=nse, index_dtype=index_dtype)
  return _lowerings.coo_fromdense_gpu_lowering(
      ctx, mat, nnz=nse, index_dtype=index_dtype,
      target_name_prefix=target_name_prefix)

