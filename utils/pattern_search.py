import re

def pattern_search(patterns: str | Sequence[str], string: str) -> str | None:
  if isinstance(patterns, str):
    patterns = (patterns,)

  for pattern in patterns:
    if re.search(pattern, string):
      return pattern
  return None

