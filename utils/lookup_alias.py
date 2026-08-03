import sys
from typing import Any

def lookup_alias(
    the_object: Any,
    infer_from_attributes: bool = True,
    allow_outdated: bool = False,
    allow_relative: bool = False,
) -> ModuleAttributePath | LocalNamePath | None:
  """Retrieves an alias for this object, if possible.

  This function checks if an alias has been registered for this object, and also
  makes sure the object is still available at that alias. It optionally also
  tries to infer a fallback alias using __module__ and __qualname__ attributes.

  Args:
    the_object: Object to get a well-known alias for.
    infer_from_attributes: Whether to use __module__ and __qualname__ attributes
      to infer an alias if no explicit path is registered.
    allow_outdated: If True, return old aliases even if the object is no longer
      accessible at this path. (For instance, if the module was reloaded after
      this class/function was defined.)
    allow_relative: If True, return aliases that are local to the current
      `relative_alias_names` context if possible.

  Returns:
    A path at which we can find this object, or None if we do not have a path
    for it (or if the path is no longer correct).
  """
  if the_object is None:
    # None itself should never have an alias. Checking for it here lets us
    # easily catch the "broken alias" case in `retrieve` below.
    return None

  alias_env = _alias_environment.get()
  # Is this object in the local aliases? If so, return that.
  if allow_relative:
    local_aliases = _current_scope_for_local_aliases.get()
  else:
    local_aliases = None

  if local_aliases and id(the_object) in local_aliases:
    return local_aliases[id(the_object)]

  # Check for a global canonical alias.
  if id(the_object) in alias_env.aliases:
    alias = alias_env.aliases[id(the_object)]
  elif infer_from_attributes:
    # Try to unwrap it, in case it's a function-like object wrapping a function.
    unwrapped = inspect.unwrap(the_object)
    if (
        hasattr(unwrapped, "__module__")
        and hasattr(unwrapped, "__qualname__")
        and unwrapped.__qualname__ is not None
        and "<" not in unwrapped.__qualname__
    ):
      alias = ModuleAttributePath(
          unwrapped.__module__, tuple(unwrapped.__qualname__.split("."))
      )
    elif isinstance(the_object, types.ModuleType):
      alias = ModuleAttributePath(the_object.__name__, ())
    else:
      # Can't infer an alias.
      return None
  else:
    return None

  if not allow_outdated:
    if isinstance(the_object, types.MethodType):
      # Methods get different IDs on each access.
      if alias.retrieve(forgiving=True) != the_object:
        return None
    else:
      if alias.retrieve(forgiving=True) is not the_object:
        return None

  if local_aliases:
    # Check if any of the attributes along this path have a local alias.
    for split_point in reversed(range(len(alias.attribute_path))):
      parent_object = ModuleAttributePath(
          alias.module_name, alias.attribute_path[:split_point]
      ).retrieve(forgiving=True)
      if id(parent_object) in local_aliases:
        local_path_to_parent = local_aliases[id(parent_object)]
        return LocalNamePath(
            local_name=local_path_to_parent.local_name,
            attribute_path=(
                local_path_to_parent.attribute_path
                + alias.attribute_path[split_point:]
            ),
        )

    # Check if any parent module of the module in which this global alias is
    # defined has a local alias that we should use instead (e.g. using `np`
    # instead of `numpy`).
    module_parts = alias.module_name.split(".")
    submodule_path_reversed = []
    while module_parts:
      # Get an equivalent path from the parent module.
      parent_module_alias = ModuleAttributePath(
          ".".join(module_parts),
          tuple(reversed(submodule_path_reversed)) + alias.attribute_path,
      )
      # Is this a real parent module? (It probably should be unless someone
      # mucked with import paths.)
      if parent_module_alias.module_name in sys.modules:
        module_id = id(sys.modules[parent_module_alias.module_name])
        # Do we have a local alias for this parent module? And, if so, can we
        # access this particular object through the parent module in the
        # expected way?
        if (
            module_id in local_aliases
            and parent_module_alias.retrieve(forgiving=True) is the_object
        ):
          # First lookup the module in the local scope, then lookup the value
          # in the module.
          local_path_to_module = local_aliases[module_id]
          return LocalNamePath(
              local_name=local_path_to_module.local_name,
              attribute_path=(
                  local_path_to_module.attribute_path
                  + parent_module_alias.attribute_path
              ),
          )
      submodule_path_reversed.append(module_parts.pop())

  return alias

