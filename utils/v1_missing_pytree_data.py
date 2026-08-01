
def v1_missing_pytree_data(
    name: str, is_dir: bool = False, is_critical: bool = False
) -> None:
  """Saves a checkpoint and removes data files or directories."""
  prefix = 'dir' if is_dir else 'file'
  alteration_type = (
      'critical_metadata_alterations'
      if is_critical
      else 'non_critical_metadata_alterations'
  )
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v1_checkpoints'
      / 'composite_checkpoint'
      / alteration_type
      / f'missing_pytree_data_{prefix}_{name}'
  )
  generate_v1_checkpoint(path)

  target_path = path / 'state'
  if is_dir:
    (target_path / name).rmtree()
  else:
    (target_path / name).unlink()

