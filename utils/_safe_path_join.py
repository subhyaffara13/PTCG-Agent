
def _safe_path_join(base: epath.Path, rel_path: str) -> epath.Path | None:
  """Joins ``rel_path`` onto ``base`` iff the result stays within ``base``.

  Rejects empty strings, absolute paths (including Windows drive-prefixed
  paths), and any path whose resolved form escapes ``base`` via ``..``
  components or symlinks. Returns ``None`` for unsafe inputs so callers can
  fail closed.

  Args:
    base: The base directory that the resulting path must be contained within.
    rel_path: A peer-supplied relative path. Treated as untrusted.

  Returns:
    ``base / rel_path`` on success, or ``None`` if ``rel_path`` is unsafe.
  """
  if not rel_path:
    return None
  # Reject absolute paths. ``os.path.isabs`` covers POSIX roots and (on
  # Windows) drive-prefixed paths; ``splitdrive`` catches e.g. ``C:foo`` which
  # is technically relative but still anchored off ``base``.
  if os.path.isabs(rel_path) or os.path.splitdrive(rel_path)[0]:
    return None
  try:
    base_real = os.path.realpath(str(base))
    candidate_real = os.path.realpath(os.path.join(base_real, rel_path))
  except OSError:
    return None
  try:
    common = os.path.commonpath([base_real, candidate_real])
  except ValueError:
    # Different drives on Windows, or otherwise incomparable.
    return None
  if common != base_real:
    return None
  return base / rel_path

