from typing import Callable

def fun_name(fun: Callable, default_name: str = "<unnamed function>") -> str:
  name = getattr(fun, "__name__", None)
  if name is not None:
    return name
  if isinstance(fun, partial):
    return fun_name(fun.func)
  else:
    return default_name

