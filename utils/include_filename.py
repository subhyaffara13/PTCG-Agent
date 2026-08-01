
def include_filename(filename: str) -> bool:
  return not any(_path_starts_with(filename, path) for path in _exclude_paths)

