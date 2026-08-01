
def is_partial_save_path(
    path: path_types.Path, allow_tmp_dir: bool = False
) -> bool:
  if allow_tmp_dir:
    return PARTIAL_SAVE_SUFFIX in path.name
  else:
    return path.name.endswith(PARTIAL_SAVE_SUFFIX)

