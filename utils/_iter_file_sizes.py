
def _iter_file_sizes(path: epath.Path) -> Iterator[tuple[str, int]]:
  """Yields (leaf_name, size_bytes) for every file under path; logs IO errors."""
  try:
    children = list(path.iterdir())
  except OSError as e:
    logging.warning("inventory: cannot iterdir %s: %s", path, e)
    return
  for child in children:
    if child.is_dir():
      yield from _iter_file_sizes(child)
      continue
    try:
      size = child.stat().length
    except (OSError, AttributeError) as e:
      logging.warning("inventory: cannot stat %s: %s", child, e)
      continue
    yield child.name, size

