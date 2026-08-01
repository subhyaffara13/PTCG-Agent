
def _save_main_ckpt_file(
  target: bytes,
  has_mpa: bool,
  paths: tuple[str, str],
  base_path: str,
  step: int,
  keep: int,
  overwrite: bool,
  keep_every_n_steps: int | None,
  ckpt_start_time: float,
):
  """Save the main checkpoint file via file system."""
  ckpt_tmp_path, ckpt_path = paths
  io.makedirs(os.path.dirname(ckpt_path))

  with io.GFile(ckpt_tmp_path, 'wb') as fp:
    fp.write(target)

  # Postpone the commitment of checkpoint to after MPA writes are done.
  if not has_mpa:
    _save_commit(
      ckpt_tmp_path,
      ckpt_path,
      base_path,
      keep,
      overwrite,
      keep_every_n_steps,
      ckpt_start_time,
      has_mpa=False,
      write_commit_success=False,
    )

