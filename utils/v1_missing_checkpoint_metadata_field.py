
def v1_missing_checkpoint_metadata_field(
    field_to_remove: str,
) -> None:
  """Saves V1 checkpoint and removes a field from _CHECKPOINT_METADATA."""
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v1_checkpoints'
      / 'composite_checkpoint'
      / 'non_critical_metadata_alterations'
      / f'missing_{field_to_remove}_metadata'
  )
  generate_v1_checkpoint(path)
  delete_checkpoint_metadata_field(path, field_to_remove)

