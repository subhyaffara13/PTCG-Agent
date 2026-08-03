from typing import Callable

def use_cpp_method(is_enabled: bool = True) -> Callable[[T], T]:
  """A decorator excluding methods from the set that are forwarded to C++ class."""
  if not isinstance(is_enabled, bool):
    raise TypeError("``is_enabled`` must be a bool")
  def decorator(f):
    if is_enabled:
      original_func = _original_func(f)
      original_func._use_cpp = True  # pyrefly: ignore[missing-attribute]
    return f
  return decorator

