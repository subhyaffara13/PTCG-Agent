
def _async_copy_scales_to_tmem_lowering_rule_wg(*args, **kwargs):
  return _async_copy_to_tmem_lowering_rule(
      mgpu.dialect.async_store_scales_smem_to_tmem,
      *args,
      **kwargs,
  )

