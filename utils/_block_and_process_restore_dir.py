import logging
import os
import time

def _block_and_process_restore_dir(
    local_checkpoint_directory: epath.Path,
    *,
    timeout_seconds: int = 300,
) -> bool:
  """Block until a `.restore` marker appears, then normalize it.

  Args:
    local_checkpoint_directory: The local checkpoint directory.
    timeout_seconds: The timeout in seconds.

  Returns:
    `True` if a restore marker or no-checkpoint marker was processed.

  Raises:
    TimeoutError: if no .restore marker is found within the timeout.

  MTC creates a `*.restore` symlink to the directory and Orbax renames it into
  the numeric step directory the backend already understands.
  """
  local_checkpoint_directory = epath.Path(local_checkpoint_directory)

  def _remove_restore_marker(marker_path: epath.Path) -> None:
    try:
      marker_path.unlink()
    except FileNotFoundError:
      pass

  for elapsed_seconds in range(timeout_seconds):
    marker_paths = sorted(
        local_checkpoint_directory.glob('*.restore'), key=lambda p: p.name
    )
    files = [f.name for f in marker_paths]
    if files:
      logging.vlog(1, 'block_and_process_restore_dir: restore files: %s', files)
    elif elapsed_seconds % 60 == 0:
      logging.info(
          'Waiting for MTC restore marker in %s... elapsed=%ds',
          local_checkpoint_directory,
          elapsed_seconds,
      )
    restore_markers = []
    no_checkpoint_markers = []
    for marker_path in marker_paths:
      step = _extract_step(marker_path.name)
      # Replicator writes a zero-sized file for "no checkpoint" and a symlink
      # for an actual restore marker.
      if step == '0' and marker_path.is_file():
        no_checkpoint_markers.append(marker_path)
      else:
        restore_markers.append((int(step), marker_path))

    if restore_markers:
      step, marker_path = max(restore_markers, key=lambda item: item[0])
      step_dir = local_checkpoint_directory / str(step)
      os.replace(marker_path, step_dir)
      logging.info(
          'Found a restore directory at step %s and renamed it to %s.',
          step,
          step_dir,
      )
      for stale_marker_path in [
          p for _, p in restore_markers if p != marker_path
      ] + no_checkpoint_markers:
        _remove_restore_marker(stale_marker_path)
        logging.vlog(
            1, 'Removed stale MTC restore marker %s.', stale_marker_path
        )
      return True

    if no_checkpoint_markers:
      for marker_path in no_checkpoint_markers:
        _remove_restore_marker(marker_path)
        logging.info(
            'Found MTC no-checkpoint restore marker %s and removed it.',
            marker_path,
        )
      return True
    time.sleep(1)
  raise TimeoutError(
      f'{timeout_seconds} seconds have passed but no .restore file was found.'
  )

