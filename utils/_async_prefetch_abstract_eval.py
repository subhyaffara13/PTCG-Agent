
def _async_prefetch_abstract_eval(ref, *args, **params):
  del args, params  # Unused.
  _check_ref(ref, "ref", gpu_core.GMEM)
  return (), {state.ReadEffect(0)}

