import re

def _include_path_regex() -> re.Pattern[str]:
  patterns = [f'^{re.escape(path)}' for path in _include_paths]
  patterns.append('_test.py$')
  return re.compile('|'.join(patterns))

