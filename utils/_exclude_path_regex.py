
def _exclude_path_regex() -> re.Pattern[str]:
  # The regex below would not handle an empty set of exclusions correctly.
  assert len(_exclude_paths) > 0
  return re.compile('|'.join(f'^{re.escape(path)}' for path in _exclude_paths))

