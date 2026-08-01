
def load_checkpointables_async(
    path: path_types.PathLike,
    abstract_checkpointables: (
        dict[str, AbstractCheckpointable]
        | CheckpointMetadata[dict[str, AbstractCheckpointable]]
        | None
    ) = None,
) -> async_types.AsyncResponse[dict[str, Checkpointable]]:
  """Loads checkpointables asynchronously. Not yet implemented."""
  del path, abstract_checkpointables
  raise NotImplementedError('Asynchronous loading is not yet supported.')

