
def _playthrough_match(filename, regex):
  """Returns the specified value fromm the playthrough."""
  with open(filename, "r", encoding="utf-8") as f:
    data = f.read()
  return re.search(regex, data, re.MULTILINE)

