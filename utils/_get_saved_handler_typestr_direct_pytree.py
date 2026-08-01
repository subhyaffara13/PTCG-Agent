
def _get_saved_handler_typestr_direct_pytree(
    checkpoint_metadata: InternalCheckpointMetadata,
) -> str | None:
  """Reads from the checkpoint metadata to get saved handler typestrs."""
  if isinstance(checkpoint_metadata.item_handlers, str):
    return checkpoint_metadata.item_handlers
  return None

