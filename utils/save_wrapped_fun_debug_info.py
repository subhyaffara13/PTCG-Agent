
def save_wrapped_fun_debug_info(wrapper: Callable,
                                dbg: core.DebugInfo) -> None:
  setattr(wrapper, "__fun_debug_info__", dbg)

