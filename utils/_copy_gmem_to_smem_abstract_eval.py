
def _copy_gmem_to_smem_abstract_eval(src, dst, barrier, *args, **params):
  del args, params  # Unused.
  _check_ref(src, "src", gpu_core.GMEM)
  _check_ref(dst, "dst", gpu_core.SMEM)
  _check_ref(barrier, "barrier", gpu_core.SMEM)
  return (), {state.ReadEffect(0), state.WriteEffect(1)}

