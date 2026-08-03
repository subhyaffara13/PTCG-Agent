import sys

def reload_workspace(
    source: g3_utils.Source | None = None,
    *,
    restrict: py_utils.StrOrStrList | None = None,
    verbose: bool = False,
    reload_mode: (
        inplace_reload.ReloadMode | str
    ) = inplace_reload.ReloadMode.INVALIDATE,
) -> None:
  """Reload all modified files in the current workspace.

  This function look at all edited files in the given workspace which are also
  imported and reload them.

  This is a no-op if the source is not a user workspace.

  Args:
    source: Same as `ecolab.adhoc`
    restrict: Same as `ecolab.adhoc`
    verbose: Same as `ecolab.adhoc`
    reload_mode: Same as `ecolab.adhoc`
  """

  from etils import g3_utils  # pylint: disable=g-import-not-at-top
  from etils.ecolab import adhoc_imports  # pylint: disable=g-import-not-at-top

  # Normalize inputs
  citc_info = g3_utils.citc_info_from_source(source)
  if isinstance(citc_info, g3_utils.PendingCl):
    citc_info = citc_info.workspace
  restrict = py_utils.normalize_str_to_list(restrict)

  # TODO(epot): When loading from workspace, then from HEAD, how to detect
  # which files should be reloaded ?
  # Especially when there's 2 different `ecolab.adhoc` scope!
  # Could detect all modules that are adhoc-imported (through the
  # `module.__file__` and reload them)
  if not isinstance(citc_info, g3_utils.Workspace):
    if prev_modules := _find_modules_imported_in_different_source(source):
      prev_module_name = next(iter(prev_modules))
      prev_source = sys.modules[prev_module_name]._etils_workspace_reload_source  # pylint: disable=protected-access
      raise ValueError(
          f'Source was changed from {prev_source!r} to {source!r}.'
          ' `reload_workspace=True` cannot auto-infer which modules to reload.'
          ' Please restart your kernel.'
      )
    else:
      return

  # Step 1: List all modules to reload
  modules_to_reload = _get_modules_to_reload(
      restrict=restrict,
      citc_info=citc_info,
  )
  if not modules_to_reload:
    return

  # Step 2: Reload
  with adhoc_imports.adhoc(
      source,
      reload=modules_to_reload,
      restrict=restrict,
      restrict_reload=False,
      reload_recursive=False,
      reload_mode=reload_mode,
      verbose=verbose,
      collapse_prefix=f'Reload workspace ({len(modules_to_reload)} modules): ',
  ):
    for module_name in modules_to_reload:
      module = importlib.import_module(module_name)
      module._etils_workspace_reload_source = source  # pylint: disable=protected-access

  # Step 3: Replace the reloaded modules in the Colab kernel.
  update_global_namespace(reload=modules_to_reload, verbose=verbose)

