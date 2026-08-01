
def _wait_smem_to_gmem_abstract_eval(n, *, wait_read_only):
  del n, wait_read_only  # Unused.
  return (), {gpu_core._memory_effect}

