
def _get_batching_group(factor: str) -> str:
  """Extracts the batching group from a factor for leading batching dimensions."""
  return factor[1:] if len(factor) > 1 else "0"

