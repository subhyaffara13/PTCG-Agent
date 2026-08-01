
def _has_pytree_metadata_file(path: epath.Path) -> bool:
  """Returns True if path contains `_METADATA` or `checkpoint` file."""
  return (path / PYTREE_METADATA_FILE).exists() or _has_msgpack_metadata_file(
      path
  )

