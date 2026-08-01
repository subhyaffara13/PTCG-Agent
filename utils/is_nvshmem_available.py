
def is_nvshmem_available() -> bool:
    r"""
    is_nvshmem_available() -> bool

    Check if NVSHMEM (CUDA) or rocSHMEM (ROCm) is available in the current
    build and usable at runtime. On ROCm, rocSHMEM ``VERSION`` must be at
    least 3.3.0 (see ``rocshmem/rocshmem.hpp``).
    """
    try:
        from torch._C._distributed_c10d import _is_nvshmem_available
    except ImportError:
        # Not all builds have NVSHMEM support.
        return False

    # Check if NVSHMEM is available on current system.
    return _is_nvshmem_available()


def is_nvshmem_available():
  try:
    nvshmem_bc_path = os.environ["MOSAIC_GPU_NVSHMEM_BC_PATH"]
  except KeyError:
    return False
  if nvshmem_so_path := os.environ.get("MOSAIC_GPU_NVSHMEM_SO_PATH", ""):
    try:
      # This both ensures that the file exists, and it populates the dlopen
      # cache, helping XLA find the library even if the RPATH is not right...
      ctypes.CDLL(nvshmem_so_path)
    except OSError:
      return False
  xla_flags = os.environ.get("XLA_FLAGS", "")
  return (
      os.path.exists(nvshmem_bc_path)
      and "--xla_gpu_experimental_enable_nvshmem" in xla_flags
  )

