
def format_tcgen05_sparse_metadata(meta, operand_dtype):
  """Formats the sparse metadata for tcgen05.mma into the expected format.

  See
  https://docs.nvidia.com/cuda/parallel-thread-execution/#tcgen05-sparse-matrices-sparsity-selector-kind-f16-m128-256
  for the documentation of the required layouts. The array can be copied into
  SMEM, from where ``plgpu.async_copy_sparse_metadata_to_tmem`` can be used to
  copy it over to TMEM. The formatting of the array depends on the data type of
  the operands to the sparse MMA operation.

  Args:
    meta: Metadata of shape (M, K // 4, 2).
    dtype: Data type of MMA operands.
  """
  if meta.dtype != dtypes.uint2:
    raise ValueError(f"Expected metadata dtype to be uint2, got: {meta.dtype}")
  if meta.ndim != 3:
    raise ValueError(
        "Expected metadata to be 3-dimensional (M, K // 4, 2), but it is"
        f" {meta.ndim}D"
    )
  m, k, _2 = meta.shape
  if _2 != 2:
    raise ValueError(
        "Expected the trailing dimension of the metadata to be 2, got:"
        f" {meta.shape[-1]}"
    )
  k *= 2
  bitsize = dtypes.itemsize_bits(operand_dtype)
  if bitsize == 8:
    meta_tiled = meta.reshape(m // 128, 128, k // 64, 64).transpose(0, 2, 1, 3)
  elif bitsize == 16:
    meta_tiled = meta.reshape(m // 128, 8, 2, 8, k // 64, 4, 2, 8).transpose(0, 4, 1, 6, 3, 5, 2, 7)
  else:
    raise NotImplementedError(
        f"Sparse metadata format not implemented for {operand_dtype=}"
    )
  return meta_tiled.reshape(m // 128, k // 64, 128, 64)

