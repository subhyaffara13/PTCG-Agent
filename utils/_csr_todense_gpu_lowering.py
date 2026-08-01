
def _csr_todense_gpu_lowering(ctx, data, indices, indptr, *, shape, target_name_prefix):
  data_aval, indices_aval, _ = ctx.avals_in
  dtype = data_aval.dtype
  if not (np.issubdtype(dtype, np.floating) or np.issubdtype(dtype, np.complexfloating)):
    warnings.warn(f"csr_todense cusparse/hipsparse lowering not available for {dtype=}. "
                  "Falling back to default implementation.", CuSparseEfficiencyWarning)
    return _csr_todense_lowering(ctx, data, indices, indptr, shape=shape)
  return [_lowerings.csr_todense_gpu_lowering(
      ctx, data, indices, indptr, shape=shape,
      target_name_prefix=target_name_prefix)]

