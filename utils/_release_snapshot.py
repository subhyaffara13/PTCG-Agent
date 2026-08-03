import logging
from typing import Optional

def _release_snapshot(
    checkpoint_dir: epath.Path,
    step: int,
    step_name_format: step_lib.NameFormat[step_lib.Metadata],
    snapshot_dir: Optional[epath.Path] = None,
    *,
    ignore_file_not_found_error: bool | None = None,
):
  """Releases snapshot by deleting the snapshot of the checkpoint."""
  if multihost.process_index() == 0:
    logging.info('Releasing snapshot at step: %d.', step)
    if snapshot_dir is None:
      snapshot_dir = checkpoint_dir / _SNAPSHOTS
    snapshot_path = snapshot_dir / step_name_format.build_name(step)
    snapshot_impl = snapshot_lib.create_instance(checkpoint_dir, snapshot_path)
    with _manage_snapshot_file_not_found(
        ignore_errors=ignore_file_not_found_error,
        formatted_message=(
            f'Ignoring error when releasing snapshot for step: {step}'
        ),
    ):
      asyncio_utils.run_sync(snapshot_impl.release_snapshot())

