import sys

def _find_modules_imported_in_different_source(
    source: g3_utils.Source,
) -> set[str]:
  """Extract all modules imported in a different source."""
  sentinel = object()
  other_previous_modules = set()
  for module_name, module in sys.modules.items():
    old_source = inspect.getattr_static(
        module, '_etils_workspace_reload_source', sentinel
    )
    if old_source is sentinel:
      continue
    if old_source != source:
      other_previous_modules.add(module_name)
  return other_previous_modules

