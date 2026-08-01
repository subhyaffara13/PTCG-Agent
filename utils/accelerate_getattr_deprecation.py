
def accelerate_getattr_deprecation(module: ModuleType, name: str) -> None:
  """Accelerate the deprecation of a module-level attribute.

  Raises an AttributeError instead of a DeprecationWarning upon attribute access.
  Used in Google-internal code to implement faster deprecation.
  """
  message, _ = module._deprecations[name]
  module._deprecations[name] = (message, None)

