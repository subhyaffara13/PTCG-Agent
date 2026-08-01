
def get_memory_space_idx(space: mosaic_gpu_core.MemorySpace) -> int:
  if space is pallas_core.MemorySpace.DEFAULT:
    return IDX_BY_GPU_MEMORY_SPACE[mosaic_gpu_core.MemorySpace.SMEM]
  return IDX_BY_GPU_MEMORY_SPACE[space]

