
def _async_copy_to_tmem_abstract_eval(smem_ref, tmem_ref, *_args, **_kwargs):
  if smem_ref.memory_space != gpu_core.MemorySpace.SMEM:
    raise ValueError("async_copy_scales_to_tmem source must be an SMEM ref")
  if tmem_ref.memory_space != gpu_core.MemorySpace.TMEM:
    raise ValueError("async_copy_scales_to_tmem target must be a TMEM ref")
  return (), {state_types.ReadEffect(0), state_types.WriteEffect(1)}

