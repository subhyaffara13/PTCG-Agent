
def _checkpointables_metadata_impl(
    layout: checkpoint_layout.CheckpointLayout,
    path: path_types.Path,
) -> CheckpointMetadata[dict[str, AbstractCheckpointable]]:
  """Shared implementation for checkpointables_metadata."""

  async def _load_metadata() -> (
      metadata_types.CheckpointMetadata[dict[str, AbstractCheckpointable]]
  ):
    return await layout.checkpointables_metadata(path)

  checkpoint_metadata = asyncio_utils.run_sync(_load_metadata())
  validation.validate_abstract_checkpointables(checkpoint_metadata.metadata)
  return checkpoint_metadata

