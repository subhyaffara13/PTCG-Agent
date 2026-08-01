
def _parse_key(key: str) -> Tuple[str, Optional[int]]:
  """Parse a ConfigDict key into to it's initial part and index (if any)."""
  key = key.split('.')[0]
  index_match = re.match(r'(.*)\[([0-9]+)\]', key)
  if index_match:
    key = index_match.group(1)
    index = int(index_match.group(2))
  else:
    index = None
  return key, index

