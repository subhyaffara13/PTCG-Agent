
def _module_and_class_name(cls) -> tuple[str, str]:
  """Returns the module and class name of the given class instance."""
  return cls.__module__, cls.__qualname__

