
def _get_final_directory(tmp_path: epath.Path) -> epath.Path:
  if (suffix_idx := tmp_path.name.find(TMP_DIR_SUFFIX)) == -1:
    raise ValueError(f'Expected {tmp_path} to end with "{TMP_DIR_SUFFIX}".')
  return tmp_path.parent / tmp_path.name[:suffix_idx]

