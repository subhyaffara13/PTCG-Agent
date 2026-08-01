
def _get_tmp_directory(final_path: epath.Path) -> epath.Path:
  # Path may not be completely unique if a preemption occurs. We rely on the
  # existing tmp directory being deleted elsewhere.
  return final_path.parent / (final_path.name + TMP_DIR_SUFFIX)

