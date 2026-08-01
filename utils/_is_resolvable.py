
def _is_resolvable(*axis_names: str | None) -> bool:
  """Checks if given sharding axis names resolve unambiguously."""
  assert len(axis_names) >= 2, "At least two axis names expected."
  return len({a for a in axis_names if a is not None}) <= 1

