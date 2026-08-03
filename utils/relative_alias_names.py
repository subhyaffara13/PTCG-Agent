from typing import Any, Callable

def relative_alias_names(
    relative_scope: Mapping[str, Any] | Literal["magic"],
    predicate: Callable[[Any, LocalNamePath], bool] = default_well_known_filter,
) -> contextlib.AbstractContextManager[None]:
  """Context manager that makes `lookup_alias` return relative aliases.

  Args:
    relative_scope: A dictionary mapping in-scope names to their values, e.g.
      `globals()` or `{**globals(), **locals()}`. Objects that are reachable
      from this scope will have aliases that reference the keys in this dict.
      Alternatively, can be the string "magic", in which case we will walk the
      stack and use the `{**globals(), **locals()}` of the caller. ("magic" is
      only recommended for interactive usage.)
    predicate: A filter function to check if an object should be given an alias.

  Returns:
    A context manager in which `lookup_alias` will try to return relative
    aliases when `allow_relative=True`.
  """
  if relative_scope == "magic":
    # Infer the scope by walking the stack. 1 is the caller's frame.
    caller_frame_info = inspect.stack()[1]
    relative_scope = collections.ChainMap(
        caller_frame_info.frame.f_globals,
        caller_frame_info.frame.f_locals,
    )

  local_alias_map = {}

  assert isinstance(relative_scope, Mapping)
  for key, value in relative_scope.items():
    path = LocalNamePath(key, ())
    if predicate(value, path):
      local_alias_map[id(value)] = path

  return _current_scope_for_local_aliases.set_scoped(local_alias_map)

