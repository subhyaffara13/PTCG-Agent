from typing import Any

def prefix_filter(include: str, excludes: tuple[str, ...] = ()):
  """Builds a filter that only defines aliases within a given prefix."""

  def is_under_prefix(path: str, prefix: str):
    return path == prefix or path.startswith(prefix + ".")

  def predicate(the_object: Any, path: ModuleAttributePath) -> bool:
    if not default_well_known_filter(the_object, path):
      return False
    if not is_under_prefix(str(path), include):
      return False
    if any(is_under_prefix(str(path), exclude) for exclude in excludes):
      return False
    if (
        hasattr(the_object, "__module__")
        and the_object.__module__
        and not is_under_prefix(the_object.__module__, include)
    ):
      return False
    return True

  return predicate

