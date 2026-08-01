
def _async_copy_scales_to_tmem_lowering_rule(*args, **kwargs):
  return _async_copy_to_tmem_lowering_rule(
      tcgen05.async_copy_scales_smem_to_tmem, *args, **kwargs
  )

