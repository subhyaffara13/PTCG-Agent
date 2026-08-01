
def nested_id_sample(ids: Any, limit: int = 4) -> str:
  """Returns a compact sample of grouped device ids for topology logging."""
  ids = tuple(tuple(int(device_id) for device_id in group) for group in ids)
  if len(ids) <= limit:
    return str(ids)
  return f'{ids[:limit]} ... ({len(ids)} groups total)'

