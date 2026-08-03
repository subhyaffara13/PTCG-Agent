from typing import Any

def _get_module_method(module, method: tp.Callable[..., Any] | str | None):
  """Get a callable method from the module, or raise TypeError."""
  if method is None:
    method = '__call__'

  if isinstance(method, str):
    attribute_name = method
    method = getattr(type(module), attribute_name)
    if not callable(method):
      class_name = type(module).__name__
      raise TypeError(
        f"'{class_name}.{attribute_name}' must be a callable, got"
        f' {type(method)}.'
      )
  if not callable(method):
    class_name = type(module).__name__
    raise TypeError(
      f"'{method}' must be a callable, got {type(method)}."
    )

  return method

