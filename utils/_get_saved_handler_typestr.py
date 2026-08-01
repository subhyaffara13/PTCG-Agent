
def _get_saved_handler_typestr(
    checkpointable_name: str,
    checkpoint_metadata: InternalCheckpointMetadata,
) -> str | None:
  """Reads from the checkpoint metadata to get saved handler typestrs."""
  if isinstance(checkpoint_metadata.item_handlers, dict) and (
      checkpointable_name in checkpoint_metadata.item_handlers
  ):
    return checkpoint_metadata.item_handlers[checkpointable_name]
  return None

