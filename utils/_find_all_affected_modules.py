
def _find_all_affected_modules(
    *,
    module_names: list[str],
    restrict: list[str],
) -> set[str]:
  """Find all affected modules."""
  if not module_names:
    return set()

  all_module_deps = module_deps_utils.get_all_module_deps()

  restrict_exact = set(restrict)
  restrict_prefix = tuple(f'{r}.' for r in restrict)

  def _filter_restrict(names: Iterable[str]) -> list[str]:
    # etils modifications are not reloaded (etils is used in too many places)
    names = [n for n in names if not n.startswith(_SKIP_RELOAD)]
    if not restrict:
      return names
    names = [
        n for n in names if n in restrict_exact or n.startswith(restrict_prefix)
    ]
    return names

  module_names = _filter_restrict(module_names)

  affected_modules = set(module_names)
  modules_to_process = set(module_names)
  visited = set()

  while modules_to_process:
    module_name = modules_to_process.pop()
    if module_name in visited:
      continue
    visited.add(module_name)
    module_deps = all_module_deps[module_name]

    imported_in = _filter_restrict(module_deps.imported_in)
    modules_to_process.update(imported_in)
    affected_modules.update(imported_in)
  return affected_modules

