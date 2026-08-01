
def register_inclusion(path: str):
  _include_paths.append(path)
  _include_path_regex.cache_clear()
  is_user_filename.cache_clear()

