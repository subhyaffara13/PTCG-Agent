from typing import Any

def lookup_treescope_handler_for_type(
    candidate_type: type[Any],
) -> renderers.TreescopeNodeHandler | None:
  """Looks up a treescope handler for the given type.

  This function can be used to look up a treescope handler for an object using
  the global registry `TREESCOPE_HANDLER_REGISTRY`. The handler will be looked
  up by the type of the given object, any of its base classes, or any virtual
  base classes listed in `VIRTUAL_BASE_CLASSES`.

  This function does NOT check for methods on the type; those should be checked
  separately.

  Args:
    candidate_type: The type to look up a handler for.

  Returns:
    A treescope handler for the given type, or None if no handler was found.
  """
  return _lookup_by_mro(TREESCOPE_HANDLER_REGISTRY, candidate_type)

