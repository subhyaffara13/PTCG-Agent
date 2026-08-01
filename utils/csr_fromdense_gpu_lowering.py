
def csr_fromdense_gpu_lowering(ctx, mat, *, nnz, index_dtype, target_name_prefix):
  mat_aval, = ctx.avals_in
  rows, cols = mat_aval.shape
  buffer_size, opaque = _get_module(target_name_prefix).build_csr_fromdense_descriptor(
      mat_aval.dtype, np.dtype(index_dtype), rows, cols, nnz)
  buffer_aval = core.ShapedArray(shape=(buffer_size,), dtype=np.int8)
  sub_ctx = ctx.replace(avals_out=[*ctx.avals_out, buffer_aval])
  rule = ffi.ffi_lowering(f"{target_name_prefix}sparse_csr_fromdense_ffi")
  return rule(sub_ctx, mat, opaque=opaque)[:3]

