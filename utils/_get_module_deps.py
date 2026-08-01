
def _get_module_deps(
    all_module_deps: dict[str, _ModuleDeps], module_name: str
) -> _ModuleDeps:
  if module_name not in all_module_deps:
    all_module_deps[module_name] = _ModuleDeps(name=module_name)
  return all_module_deps[module_name]

