
def scan_checkpoint(path: epath.Path) -> CheckpointInventory:
  """Walks `path` recursively and returns file counts + size totals.

  Scan failures log a warning rather than raise, so a benchmark that completed
  successfully isn't marked failed just because the post-save walk hit an IO
  error.

  Args:
    path: The checkpoint directory to inventory.

  Returns:
    The inventory, or an empty one if the path doesn't exist.
  """
  path = epath.Path(path)
  if not path.exists():
    return CheckpointInventory()

  total_bytes = small_file_count = largest = 0
  smallest = -1
  file_count = 0
  format_counts: dict[str, int] = {}
  for name, size in _iter_file_sizes(path):
    file_count += 1
    total_bytes += size
    if size < _SMALL_FILE_THRESHOLD_BYTES:
      small_file_count += 1
    largest = max(largest, size)
    smallest = size if smallest < 0 else min(smallest, size)
    bucket = _classify_file(name)
    format_counts[bucket] = format_counts.get(bucket, 0) + 1

  return CheckpointInventory(
      total_bytes=total_bytes,
      file_count=file_count,
      small_file_count=small_file_count,
      small_file_pct=(small_file_count / file_count) if file_count else 0.0,
      largest_file_bytes=largest,
      smallest_file_bytes=max(smallest, 0),
      format=dict(format_counts),
  )

