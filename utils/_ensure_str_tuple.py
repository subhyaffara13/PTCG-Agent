
def _ensure_str_tuple(x: str | Iterable[str]) -> tuple[str, ...]:
  """Convert x to a tuple of strings."""
  if isinstance(x, str):
    return (x,)
  else:
    return tuple(map(_ensure_str, x))

