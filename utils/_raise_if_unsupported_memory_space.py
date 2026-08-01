
def _raise_if_unsupported_memory_space(
    space: mosaic_gpu_core.MemorySpace | None,
):
  # TODO(nrink): Support more memory spaces.
  if space is not None and space not in [
      mosaic_gpu_core.MemorySpace.GMEM,
      mosaic_gpu_core.MemorySpace.SMEM,
      mosaic_gpu_core.MemorySpace.REGS,
  ]:
    raise NotImplementedError(f"Unsupported memory space: {space}")

