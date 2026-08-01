
def _filter_only_imported_modules(opened_files: Iterable[str]) -> list[str]:
  """Restrict the list of files to Python modules already in sys.modules."""
  all_opened_modules = []
  for path in opened_files:
    # TODO(epot): supports proto
    if not path.endswith('.py'):
      continue
    if module_utils.path_to_module_name(path) not in sys.modules:
      continue
    all_opened_modules.append(path)

  return all_opened_modules

