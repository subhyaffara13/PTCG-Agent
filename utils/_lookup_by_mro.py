
def _lookup_by_mro(
    registry: dict[type[Any], T], candidate_type: type[Any]
) -> T | None:
  """Looks up the given type in the given registry, or in its base classes.

  This function looks up the given type in the given registry, or in the
  registry for any base class of the given type, in method resolution order.

  If no concrete base class is found in the registry, each of the entries of
  `VIRTUAL_BASE_CLASSES` will be checked to see if it is a virtual base class.
  The first such base class that has an entry in the registry will be used.

  Args:
    registry: The registry to look up in.
    candidate_type: The type to look up.

  Returns:
    The value associated with the given type (or a base class of it) in the
    given registry, or None if no entry was found.
  """
  for supertype in candidate_type.__mro__:
    if supertype in registry:
      return registry[supertype]
  for base_class in VIRTUAL_BASE_CLASSES:
    if issubclass(candidate_type, base_class) and base_class in registry:
      return registry[base_class]
  return None

