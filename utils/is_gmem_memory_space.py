
def is_gmem_memory_space(space: mosaic_gpu_core.MemorySpace | None) -> bool:
  return space == mosaic_gpu_core.MemorySpace.GMEM

