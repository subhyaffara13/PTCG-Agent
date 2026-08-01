
def v0_generate_case(
    is_direct_checkpoint: bool,
    has_checkpoint_metadata: bool,
    has_pytree_metadata: bool,
) -> None:
  """Generates a V0 checkpoint based on parameters."""
  ckpt_type = (
      'direct_checkpoint' if is_direct_checkpoint else 'composite_checkpoint'
  )
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
      / 'v0_checkpoints'
      / ckpt_type
      / metadata_dir
      / pytree_dir
  )

  generate_v0_checkpoint(path, is_direct_checkpoint=is_direct_checkpoint)

  if not has_checkpoint_metadata:
    metadata_path = path / '_CHECKPOINT_METADATA'
    if metadata_path.exists():
      metadata_path.unlink()

  if not has_pytree_metadata:
    pytree_metadata_path = path if is_direct_checkpoint else path / 'state'
    (pytree_metadata_path / '_METADATA').unlink()

