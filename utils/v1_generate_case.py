
def v1_generate_case(
    has_checkpoint_metadata: bool,
    has_pytree_metadata: bool,
) -> None:
  """Generates a V1 checkpoint based on parameters."""
  metadata_dir = (
      'checkpoint_metadata_present'
      if has_checkpoint_metadata
      else 'checkpoint_metadata_missing'
  )
  pytree_dir = (
      'pytree_checkpointable_has_metadata'
      if has_pytree_metadata
      else 'pytree_checkpointable_missing_metadata'
  )
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v1_checkpoints'
      / 'composite_checkpoint'
      / metadata_dir
      / pytree_dir
  )

  generate_v1_checkpoint(path)

  if not has_checkpoint_metadata:
    metadata_path = path / '_CHECKPOINT_METADATA'
    if metadata_path.exists():
      metadata_path.unlink()

  if not has_pytree_metadata:
    pytree_metadata_path = path / 'state'
    (pytree_metadata_path / '_METADATA').unlink()

