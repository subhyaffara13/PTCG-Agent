
def safe_normpath(path: str) -> str:
  """Normalizes path safely to get around `io.glob()` limitations."""
  match = SCHEME_RE.match(path)
  assert match is not None
  d = match.groupdict()
  return (d['scheme'] or '') + os.path.normpath(d['path'])

