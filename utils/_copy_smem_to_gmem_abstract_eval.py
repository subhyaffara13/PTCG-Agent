
def _copy_smem_to_gmem_abstract_eval(src, dst, *args, **params):
  _check_ref(src, "src", gpu_core.SMEM)
  _check_ref(dst, "dst", gpu_core.GMEM)
  del args, params  # Unused.
  return (), {state.ReadEffect(0), state.WriteEffect(1)}

