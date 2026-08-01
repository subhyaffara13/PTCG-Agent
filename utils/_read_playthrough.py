
def _read_playthrough(filename):
  """Returns the content and the parsed arguments of a playthrough file."""
  with open(filename, "r", encoding="utf-8") as f:
    original = f.read()
  kwargs = _playthrough_params(original.splitlines())
  return original, kwargs

