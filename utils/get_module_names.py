
def get_module_names(
    restrict: py_utils.StrOrStrList, *, recursive: bool = True
) -> list[str]:
  """Returns all `sys.modules` matching the restrict name."""

  modules = py_utils.normalize_str_to_list(restrict)
  assert all('/' not in module for module in modules)

  # List all the currently loaded modules matching `modules`
  if recursive:
    modules = tuple(modules)
    return [m for m in sys.modules if m.startswith(modules)]
  else:
    modules = set(modules)
    return [m for m in sys.modules if m in modules]

