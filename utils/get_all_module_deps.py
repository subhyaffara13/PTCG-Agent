import sys

def get_all_module_deps() -> dict[str, _ModuleDeps]:
  """Construct the graph of the imported nodes."""
  # Track all modules deps
  all_module_deps = {}

  # TODO(epot): This should be optimized with caching (no need to recompute
  # the full graph at each reload). However be careful:
  # * Make sure syncing workspace re-trigger a full graph computation
  # * How to make sure the lazy-imports are properly updated
  # * Should cache be shared across adhoc calls ?

  for k, module in sys.modules.items():
    # Filter built-in, lazy-imports
    if inspect.getattr_static(module, '__file__', None) is None:
      continue

    module_deps = _get_module_deps(all_module_deps, k)

    for imported_module in module.__dict__.values():
      if not _ismodule(imported_module):
        continue

      imported_module_name = inspect.getattr_static(
          imported_module, '__name__', None
      )
      if imported_module_name is None:  # Filter lazy-imports
        continue

      imported_module_deps = _get_module_deps(
          all_module_deps, imported_module_name
      )
      module_deps.importing[imported_module_deps.name] = imported_module_deps
      imported_module_deps.imported_in[module_deps.name] = module_deps
  return all_module_deps

