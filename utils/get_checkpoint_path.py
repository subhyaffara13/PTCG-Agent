
def get_checkpoint_path(
    version: str,
    metadata_present: bool,
    is_direct_checkpoint: bool,
    is_pytree: bool,
) -> epath.Path | None:
  """Returns the path to the checkpoint for each combination of parameters."""
  if version == 'v1' and is_direct_checkpoint:
    return None  # V1 does not support direct checkpoints.

  version_dir = f'{version}_checkpoints'
  type_dir = (
      'direct_checkpoint' if is_direct_checkpoint else 'composite_checkpoint'
  )
  metadata_dir = (
      'checkpoint_metadata_present'
      if metadata_present
      else 'checkpoint_metadata_missing'
  )
  pytree_dir = (
      'pytree_checkpointable_has_metadata'
      if is_pytree
      else 'pytree_checkpointable_missing_metadata'
  )

  return (
      epath.Path(_BASE_DIR)
      / version_dir
      / type_dir
      / metadata_dir
      / pytree_dir
  )

