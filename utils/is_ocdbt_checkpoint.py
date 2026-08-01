
def is_ocdbt_checkpoint(path: epath.PathLike) -> bool:
  """Determines whether a checkpoint uses OCDBT format."""
  path = epath.Path(path)
  return (path / _OCDBT_MANIFEST_FILE).exists()

