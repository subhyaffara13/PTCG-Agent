
def _belong_to_module(obj: Any, module: types.ModuleType) -> bool:
  """Returns `True` if the instance, class, function belong to module."""
  return inspect.getattr_static(obj, "__module__", None) == module.__name__

