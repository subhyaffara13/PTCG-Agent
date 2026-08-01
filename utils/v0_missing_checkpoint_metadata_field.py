
def v0_missing_checkpoint_metadata_field(
    field_to_remove: str,
    is_direct_checkpoint: bool,
) -> None:
  """Saves V0 checkpoint and removes a field from _CHECKPOINT_METADATA."""
  ckpt_type = (
      'direct_checkpoint' if is_direct_checkpoint else 'composite_checkpoint'
  )
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v0_checkpoints'
      / ckpt_type
      / 'non_critical_metadata_alterations'
      / f'missing_{field_to_remove}_metadata'
  )
  generate_v0_checkpoint(path, is_direct_checkpoint=is_direct_checkpoint)
  delete_checkpoint_metadata_field(path, field_to_remove)

