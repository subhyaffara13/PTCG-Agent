
def _filter_recently_edited(
    *,
    citc_info: g3_utils.Workspace,
    module_paths: list[str],
) -> list[str]:
  """Only keep modules that have been updated."""
  recently_edited = []

  for module_path in module_paths:
    # TODO(epot): could also check that `sys.modules[].__file__` matches
    # `citc_info.g3_path`, otherwise, should force reload.
    module_name = module_utils.path_to_module_name(module_path)
    curr_time = (citc_info.g3_path.parent / module_path).stat().mtime
    prev_time = _MODULES_EDIT_TIME.get(module_name)

    if prev_time == curr_time:  # File already cached. No updates
      continue
    _MODULES_EDIT_TIME[module_name] = curr_time
    recently_edited.append(module_name)
  return recently_edited

