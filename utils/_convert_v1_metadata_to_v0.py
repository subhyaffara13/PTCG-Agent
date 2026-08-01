
def _convert_v1_metadata_to_v0(
    name: str,
    directory: path_types.Path | None,
    metadata: types.AbstractShardedArray,
) -> value_metadata.Metadata:
  """Wrap V1 metadata into :py:class:`~.V0Metadata`."""
  return V0Metadata(
      name=name,
      directory=directory,
      v1_metadata=metadata,
  )

