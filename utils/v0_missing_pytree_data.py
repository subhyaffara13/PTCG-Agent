
def v0_missing_pytree_data(
    name: str,
    is_direct_checkpoint: bool,
    is_dir: bool = False,
    is_critical: bool = False,
) -> None:
  """Saves a checkpoint and removes data files or directories."""
  ckpt_type = (
      'direct_checkpoint' if is_direct_checkpoint else 'composite_checkpoint'
  )
  prefix = 'dir' if is_dir else 'file'
  alteration_type = (
      'critical_metadata_alterations'
      if is_critical
      else 'non_critical_metadata_alterations'
  )
  path = (
      epath.Path(_BASE_DIR.value)
      / 'v0_checkpoints'
      / ckpt_type
      / alteration_type
      / f'missing_pytree_data_{prefix}_{name}'
  )
  generate_v0_checkpoint(path, is_direct_checkpoint=is_direct_checkpoint)

  target_path = path if is_direct_checkpoint else path / 'state'
  if is_dir:
    (target_path / name).rmtree()
  else:
    (target_path / name).unlink()

