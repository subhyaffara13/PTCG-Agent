
def _glance_num(value: float | None, fmt: str = "{:.2f}") -> str:
  """Formats a value for a glance card, or an em-dash when missing."""
  return fmt.format(value) if value is not None else "—"

