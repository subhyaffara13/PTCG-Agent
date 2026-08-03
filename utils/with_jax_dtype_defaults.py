import functools
from typing import Any, Callable

def with_jax_dtype_defaults(func: Callable[..., Any], use_defaults: bool = True):
  """Return a version of a function with outputs that match JAX's default dtypes.

  This is generally used to wrap numpy functions within tests, in order to make
  their default output dtypes match those of corresponding JAX functions, taking
  into account the state of the ``jax_enable_x64`` flag.

  Args:
    use_defaults : whether to convert any given output to the default dtype. May be
      a single boolean, in which case it specifies the conversion for all outputs,
      or may be a pytree with the same structure as the function output.
  """
  @functools.wraps(func)
  def wrapped(*args, **kwargs):
    result = func(*args, **kwargs)
    if isinstance(use_defaults, bool):
      return tree_map(to_default_dtype, result) if use_defaults else result
    else:
      f = lambda arr, use_default: to_default_dtype(arr) if use_default else arr
      return tree_map(f, result, use_defaults)
  return wrapped

