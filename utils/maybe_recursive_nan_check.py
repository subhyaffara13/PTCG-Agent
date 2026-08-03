from typing import Callable

def maybe_recursive_nan_check(
    e: Exception, fun: Callable, args, kwargs
) -> NoReturn:
  print("Invalid nan value encountered in the output of a jax.jit "
        "function. Calling the de-optimized version.")
  try:
    _ = fun(*args, **kwargs)
  except (FloatingPointError, ZeroDivisionError) as e2:
    raise e2 from None
  else:
    _raise_no_nan_in_deoptimized(e)

