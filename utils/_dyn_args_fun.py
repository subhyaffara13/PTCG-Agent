from typing import Callable

def _dyn_args_fun(fun: Callable, static_argnums: frozenset[int],
                  static_args: tuple[WrapHashably, ...], nargs: int):
  if any(isinstance(x.val, core.Tracer) for x in static_args):
    return _dyn_args_fun_uncached(fun, static_argnums, static_args, nargs)
  return _dyn_args_fun_cached(fun, static_argnums, static_args, nargs)

