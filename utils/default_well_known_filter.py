from typing import Any

def default_well_known_filter(
    the_object: Any, path: ModuleAttributePath | LocalNamePath
) -> bool:
  """Checks if an object looks like something we want to define an alias for."""

  is_function_after_unwrap = isinstance(
      inspect.unwrap(the_object), types.FunctionType
  )

  # Only define aliases for objects that are either (a) mutable or (b)
  # classes/functions/modules.
  if (
      (hasattr(the_object, "__hash__") and the_object.__hash__ is not None)
      and not isinstance(the_object, (types.ModuleType, type))
      and not is_function_after_unwrap
  ):
    return False

  # Don't allow classes and functions to be assigned to any name other than the
  # name they were given at creation time.
  if isinstance(the_object, type) or (
      is_function_after_unwrap and hasattr(the_object, "__name__")
  ):
    expected_name = the_object.__name__
    if path.attribute_path and expected_name != path.attribute_path[-1]:
      return False

  # Assume any name that starts with an underscore is private.
  if any(attr.startswith("_") for attr in path.attribute_path) or (
      isinstance(path, LocalNamePath) and path.local_name.startswith("_")
  ):
    return False

  return True

