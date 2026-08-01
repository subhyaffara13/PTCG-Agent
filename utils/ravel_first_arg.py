
def ravel_first_arg(f: Callable, unravel, debug_info: core.DebugInfo):
  return ravel_first_arg_(lu.wrap_init(f, debug_info=debug_info),
                          unravel).call_wrapped

