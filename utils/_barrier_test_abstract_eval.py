
def _barrier_test_abstract_eval(barrier, *args, **params):
  _check_ref(barrier, "barrier", gpu_core.SMEM)
  del args, params  # Unused.
  return jax_core.ShapedArray((), bool), {gpu_core._memory_effect}

