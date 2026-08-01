
def is_accelerated_attribute(module: ModuleType, name: str) -> bool:
  """Returns true if given name is accelerated.

  Raises an error if name is not a deprecated attribute in module.
  """
  return module._deprecations[name][1] is None

