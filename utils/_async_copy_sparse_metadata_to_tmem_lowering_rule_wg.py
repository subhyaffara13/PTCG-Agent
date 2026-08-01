
def _async_copy_sparse_metadata_to_tmem_lowering_rule_wg(*args, **kwargs):
  return _async_copy_to_tmem_lowering_rule(
      mgpu.dialect.async_store_sparse_metadata_smem_to_tmem,
      *args,
      **kwargs,
  )

