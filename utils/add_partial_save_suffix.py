
def add_partial_save_suffix(path: path_types.Path) -> path_types.Path:
  return path.parent / (path.name + PARTIAL_SAVE_SUFFIX)

