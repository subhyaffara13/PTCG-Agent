
def wrap_init(f: Callable, params=None, *, debug_info=None) -> WrappedFun:
  debug_info = debug_info or _missing_debug_info("linear_util.wrap_init")
  return _wrap_init(f, params, debug_info=debug_info)


def wrap_init(f: Callable, params=None, *, debug_info: DebugInfo) -> WrappedFun:
  """Wraps function `f` as a `WrappedFun`, suitable for transformation."""
  params_dict = {} if params is None else params
  params = () if params is None else tuple(sorted(params.items()))
  debug_info = debug_info._replace(result_paths=None)
  fun = WrappedFun(f, partial(f, **params_dict), (), (), params, None, debug_info)
  return fun

