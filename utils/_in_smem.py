
def _in_smem(spec: pallas_core.BlockSpec) -> bool:
  return spec.memory_space in (pallas_core.MemorySpace.DEFAULT, gpu_core.SMEM, None)

