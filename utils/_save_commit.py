import logging
import os
import time

def _save_commit(
  ckpt_tmp_path: str,
  ckpt_path: str,
  base_path: str,
  keep: int,
  overwrite: bool,
  keep_every_n_steps: int | None,
  ckpt_start_time: float,
  has_mpa: bool,
  write_commit_success: bool,
  async_manager: AsyncManager | None = None,
) -> None:
  """Commit changes after saving checkpoints to disk.

  This function does the following, sequentially:
    1. Make sure all ckpt writing finishes, and rename them from temp path to
    the final path.
    2. Remove newer checkpoints (files that ordered larger than this save) if
    `overwrite=True`.
    3. Remove old checkpoint files based on `keep` and `keep_every_n_steps`.
    4. Record program duration saved by this checkpoint.
  """
  mpa_ckpt_tmp_path, mpa_ckpt_path = (
    ckpt_tmp_path + MP_ARRAY_POSTFIX,
    ckpt_path + MP_ARRAY_POSTFIX,
  )
  # Rename the multiprocess array path once serialization and writing finished.
  if has_mpa:
    if write_commit_success:
      commit_success_path = os.path.join(mpa_ckpt_path, COMMIT_SUCCESS_FILE)
      with io.GFile(commit_success_path, 'w') as f:
        f.write(f'Checkpoint commit was successful to {mpa_ckpt_path}')
    else:
      # Commits are a two stage process (renaming the array folder and renaming
      # the main ckpt file in sequential order). We always try to overwrite
      # here because the array ckpt might be already renamed in a previously
      # interrupted commit. NOTE: io.rename does not support overwriting
      # directories via `rename` so we manually overwrite it.
      if io.exists(mpa_ckpt_path):
        logging.info('Removing outdated checkpoint at %s', mpa_ckpt_path)
        io.rmtree(mpa_ckpt_path)
      io.rename(mpa_ckpt_tmp_path, mpa_ckpt_path)
  # Commit the main checkpoint file after arrays (if any) are committed
  if async_manager:
    async_manager.wait_previous_save()
  io.rename(ckpt_tmp_path, ckpt_path, overwrite=overwrite)
  logging.info('Saved checkpoint at %s', ckpt_path)

  # Remove newer and older invalid checkpoints.
  _remove_invalid_ckpts(
    ckpt_path, base_path, keep, overwrite, keep_every_n_steps, has_mpa
  )
  # Record checkpoint-related metrics.
  ocp.utils.record_saved_duration(ckpt_start_time)
  if async_manager:
    jax.monitoring.record_event_duration_secs(
      '/jax/checkpoint/write/async/total_duration_secs',
      time.time() - ckpt_start_time,
    )

