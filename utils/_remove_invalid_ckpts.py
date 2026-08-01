
def _remove_invalid_ckpts(
  ckpt_path: str,
  base_path: str,
  keep: int,
  overwrite: bool,
  keep_every_n_steps: int | None,
  has_mpa: bool,
) -> None:
  """Clean up the checkpoint space according to `overwrite`, `keep`, and `keep_every_n_steps` parameters."""
  dir_path, prefix = os.path.split(base_path)
  checkpoint_files: list[Any] = [
    pathlib.PurePath(c) for c in _allowempty_listdir(dir_path)
  ]
  checkpoint_files = [
    os.path.join(dir_path, c)
    for c in checkpoint_files
    if c.match(f'{prefix}*') and not c.match(f'*{MP_ARRAY_POSTFIX}')
  ]
  checkpoint_files = natural_sort(checkpoint_files)

  # Remove newer checkpoints
  if overwrite and ckpt_path in checkpoint_files:
    ind = checkpoint_files.index(ckpt_path) + 1
    newer_ckpts = checkpoint_files[ind:]
    checkpoint_files = checkpoint_files[:ind]
    for path in newer_ckpts:
      logging.info('Removing checkpoint at %s', path)
      if has_mpa:
        # MPA might be removed already but the main ckpt is still there. This
        # can happen if the job is previously preempted after deleting the MPA
        # checkpoint folder and before deleting the main checkpoint.
        if io.exists(path + MP_ARRAY_POSTFIX):
          io.rmtree(path + MP_ARRAY_POSTFIX)
      _safe_remove(path)

  # Remove old checkpoint files.
  last_kept = -float('inf')
  if len(checkpoint_files) > keep:
    old_ckpts = checkpoint_files[:-keep]
    # Note: old_ckpts is sorted from oldest to newest.
    for path in old_ckpts:
      if keep_every_n_steps:
        step_number = _checkpoint_path_step(path)
        if step_number and (step_number - last_kept) >= keep_every_n_steps:
          logging.debug(
            'Not deleting %s, because last_kept=%f and keeping '
            'every %d steps.',
            path,
            last_kept,
            keep_every_n_steps,
          )
          last_kept = step_number
          continue
      logging.info('Removing checkpoint at %s', path)
      if has_mpa:
        # MPA might be removed already but the main ckpt is still there.
        if io.exists(path + MP_ARRAY_POSTFIX):
          io.rmtree(path + MP_ARRAY_POSTFIX)
      _safe_remove(path)

