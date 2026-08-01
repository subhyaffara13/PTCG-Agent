
def _update_debug_special_thread_local(_):
  if (config.debug_nans.get_local() == True or
      config.debug_infs.get_local() == True):
    _post_hook_state.set_local(_nan_check_posthook)
  else:
    _post_hook_state.set_local(None)

