
def _get_modules_to_reload(
    *,
    citc_info: g3_utils.Workspace,
    restrict: list[str],
) -> list[str]:
  """Find all modules to reload."""
  # Find the modules to reload:
  # * Load all files openned in the workspace
  # * Only keep the `.py` files which are in the `sys.modules`
  # * Check if the module has been changed since the import time.
  # * Traverse the tree of import dependencies to find out all modules affected
  #   by the changes.
  opened_files = _all_opened_files(citc_info)
  opened_module_paths = _filter_only_imported_modules(opened_files)
  edited_modules = _filter_recently_edited(
      module_paths=opened_module_paths,
      citc_info=citc_info,
  )
  modules_to_reload = _find_all_affected_modules(
      module_names=edited_modules,
      restrict=restrict,
  )
  return list(modules_to_reload)

