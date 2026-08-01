
def _checkpoint_path_step(path: str) -> float | None:
  """Returns the step number of a checkpoint path."""
  for s in SIGNED_FLOAT_RE.split(path)[::-1]:
    if SIGNED_FLOAT_RE.match(s):
      return float(s)
  return None

