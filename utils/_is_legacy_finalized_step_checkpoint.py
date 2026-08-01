
def _is_legacy_finalized_step_checkpoint(path: epath.Path) -> bool:
  return _is_legacy_step_checkpoint(path) and is_path_finalized(path)

