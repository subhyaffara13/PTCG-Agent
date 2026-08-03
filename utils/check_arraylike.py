from typing import Any

def check_arraylike(fun_name: str, *args: Any, emit_warning=False, stacklevel=3):
  """Check if all args fit JAX's definition of arraylike."""
  assert isinstance(fun_name, str), f"fun_name must be a string. Got {fun_name}"
  if any(not _arraylike(arg) for arg in args):
    pos, arg = next((i, arg) for i, arg in enumerate(args)
                    if not _arraylike(arg))
    msg = f"{fun_name} requires ndarray or scalar arguments, got {type(arg)} at position {pos}."
    if emit_warning:
      warnings.warn(msg + " In a future JAX release this will be an error.",
                    category=DeprecationWarning, stacklevel=stacklevel)
    else:
      raise TypeError(msg.format(fun_name, type(arg), pos))

