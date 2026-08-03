from typing import Callable

def unary_ufunc(func: Callable[[ArrayLike], Array]) -> ufunc:
  """An internal helper function for defining unary ufuncs."""
  func_jit = jit(func, inline=True)
  return ufunc(func_jit, name=func.__name__, nin=1, nout=1, call=func_jit)

