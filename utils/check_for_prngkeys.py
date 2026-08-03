from typing import Any

def check_for_prngkeys(fun_name: str, *args: Any):
  """Check if args don't match and none of the args have typed prng dtype"""
  arg_dtypes = [dtypes.dtype(arg) for arg in args]
  if len(set(arg_dtypes)) < 2:
    return  # Will be caught by extended dtype impl rules.
  if any(dtypes.issubdtype(dt, dtypes.prng_key) for dt in arg_dtypes):
    if len(arg_dtypes) == 1:
      raise TypeError(
        f"{fun_name} does not accept dtype {str(arg_dtypes[0])}.")
    else:
      raise TypeError(
        f"{fun_name} does not accept dtypes {', '.join(map(str, arg_dtypes))}."
      )

