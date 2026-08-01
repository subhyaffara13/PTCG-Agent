
def _has_msgpack_metadata_file(path: epath.Path) -> bool:
  return (path / _CHECKPOINT_FILE).exists()

