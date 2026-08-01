
def _pattern_cache(pattern: str) -> re.Pattern[str]:
  pattern = re.sub(r'\{(?P<name>\w+)\}', r'(?P<\g<name>>.+)', pattern)
  return re.compile(pattern)

