
def get_calling_module() -> str:
  """Returns the name of the module that's calling into this module."""
  return get_calling_module_object_and_name().module_name

