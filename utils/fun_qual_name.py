from typing import Callable

def fun_qual_name(fun: Callable) -> str:
  qual_name = getattr(fun, "__qualname__", None)
  if qual_name is not None:
    return qual_name
  if isinstance(fun, partial):
    return fun_qual_name(fun.func)
  return fun_name(fun)

