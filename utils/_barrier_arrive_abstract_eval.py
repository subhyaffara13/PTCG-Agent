
def _barrier_arrive_abstract_eval(barrier, *args, **params):
  del args, params  # Unused.
  _check_ref(barrier, "barrier", gpu_core.SMEM)
  return (), {gpu_core._memory_effect}

