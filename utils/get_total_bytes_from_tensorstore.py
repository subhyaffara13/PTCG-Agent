from typing import Any

def get_total_bytes_from_tensorstore(
    metrics: Sequence[dict[str, Any]], direction: types.IoDirection
) -> int:
  """Sums bytes_read or bytes_written from all kvstore drivers in metrics."""
  total = 0
  if direction == types.IoDirection.WRITE:
    suffix = '/bytes_written'
  elif direction == types.IoDirection.READ:
    suffix = '/bytes_read'
  else:
    raise ValueError(f'Invalid direction: {direction}')

  for m in metrics:
    if not isinstance(m, dict):
      continue
    name = m.get('name', '')
    if name.startswith('/tensorstore/kvstore/') and name.endswith(suffix):
      for val in m.get('values', []):
        if isinstance(val, dict):
          total += val.get('value', 0)
  return total

