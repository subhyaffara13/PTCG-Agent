from typing import Any

def lookup_immutability_for_type(candidate_type: type[Any]) -> bool:
  """Checks if an object is marked as immutable in the global registry.

  This function can be used to look up whether an object should be considered
  immutable for treescope according to `IMMUTABLE_TYPES_REGISTRY`. The status
  will be looked up by the type of the given object, any of its base classes, or
  any virtual base classes listed in `VIRTUAL_BASE_CLASSES`.

  Args:
    candidate_type: The type to check immutability of.

  Returns:
    True if this type is registered as immutable, False otherwise.
  """
  return bool(_lookup_by_mro(IMMUTABLE_TYPES_REGISTRY, candidate_type))

