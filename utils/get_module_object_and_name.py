import sys
from typing import Any

def get_module_object_and_name(
    globals_dict: dict[str, Any],
) -> _ModuleObjectAndName | None:
  """Returns the module that defines a global environment, and its name.

  Args:
    globals_dict: A dictionary that should correspond to an environment
      providing the values of the globals.

  Returns:
    _ModuleObjectAndName - pair of module object & module name.
    Returns None if the module could not be identified.
  """
  try:
    name = globals_dict['__name__']
    module = sys.modules[name]
  except KeyError:
    return None
  # Pick a more informative name for the main module.
  return _ModuleObjectAndName(
      module, sys.argv[0] if name == '__main__' else name
  )

