
def _humanize_gib(value_gib: float | None) -> str:
  """Humanizes a value expressed in GiB into the most readable binary unit."""
  return _humanize_bytes(None if value_gib is None else value_gib * 1024**3)

