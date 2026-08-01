
def _humanize_bytes(num_bytes: float | None) -> str:
  """Formats a byte count using the humanize library, or em-dash if missing."""
  if num_bytes is None:
    return "—"
  if abs(num_bytes) < 1024:
    return f"{num_bytes:.0f} B"
  return humanize.naturalsize(num_bytes, binary=True, format="%.2f")

