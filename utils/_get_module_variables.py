from typing import Any

def _get_module_variables(
  path: tuple[str, ...],
  variables: FrozenVariableDict,
  all_paths: set[tuple[str, ...]],
) -> tuple[MutableVariableDict, Any]:
  """A function that takes a path and variables structure and returns a

  (module_variables, submodule_variables) tuple for that path.
  _get_module_variables
  uses the `all_paths` set to determine if a variable belongs to a submodule or
  not.
  """
  module_variables = _get_path_variables(path, variables)
  submodule_variables: Any = {collection: {} for collection in module_variables}
  all_keys = {
    key for collection in module_variables.values() for key in collection
  }

  for key in all_keys:
    submodule_path = path + (key,)
    if submodule_path in all_paths:
      for collection in module_variables:
        if key in module_variables[collection]:
          submodule_variables[collection][key] = module_variables[
            collection
          ].pop(key)

  return module_variables, submodule_variables

