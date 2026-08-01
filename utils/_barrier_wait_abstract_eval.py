
def _barrier_wait_abstract_eval(barrier, *args, **params):
  _check_ref(barrier, "barrier", gpu_core.SMEM)
  del args, params  # Unused.
  return (), {gpu_core._memory_effect}

