import logging
from typing import Optional

def _snapshot_checkpoint(
    checkpoint_dir: epath.Path,
    step: int,
    step_name_format: step_lib.NameFormat[step_lib.Metadata],
    snapshot_dir: Optional[epath.Path] = None,
    *,
    set_immutable: bool | None = None,
    ignore_file_not_found_error: bool | None = None,
):
  """Uses `Snapshot` class to create a cheap "copy" of the checkpoint."""
  if multihost.process_index() != 0:
    return False

  logging.info('Snapshotting step: %d.', step)
  step_dir = step_name_format.find_step(checkpoint_dir, step).path
  if not step_dir.exists():
    raise ValueError(f'Step directory {step_dir} does not exist.')

  if snapshot_dir is None:
    snapshot_dir = checkpoint_dir / _SNAPSHOTS
  if not snapshot_dir.exists():
    try:
      snapshot_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
      raise ValueError(
          f'Failed to create snapshot directory {snapshot_dir}. Please'
          ' provide a snapshot directory instead.'
      ) from e

  snapshot_path = get_snapshot_dir_from_step_dir(step_dir, snapshot_dir)
  if epath.Path(snapshot_path).exists():
    return True
  snapshot_impl = snapshot_lib.create_instance(
      step_dir, snapshot_path, set_immutable=set_immutable
  )
  with _manage_snapshot_file_not_found(
      ignore_errors=ignore_file_not_found_error,
      formatted_message=(
          f'Ignoring error when snapshotting checkpoint for step: {step}'
      ),
  ):
    asyncio_utils.run_sync(snapshot_impl.create_snapshot())
  return True

