
def _update_debug_special_global(_):
  if config._read("jax_debug_nans") or config._read("jax_debug_infs"):
    _post_hook_state.set_global(_nan_check_posthook)
  else:
    _post_hook_state.set_global(None)

