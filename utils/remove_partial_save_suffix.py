
def remove_partial_save_suffix(path: path_types.Path) -> path_types.Path:
  return path.parent / path.name.removesuffix(PARTIAL_SAVE_SUFFIX)

