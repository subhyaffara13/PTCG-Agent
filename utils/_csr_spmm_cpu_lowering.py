
def _csr_spmm_cpu_lowering(ctx, data, outer_indices, inner_indices, rhs):
  rule = ffi.ffi_lowering("cpu_csr_sparse_dense_ffi")
  return rule(ctx, data, outer_indices, inner_indices, rhs)

