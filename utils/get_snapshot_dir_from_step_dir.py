from typing import Optional

def get_snapshot_dir_from_step_dir(
    step_dir: epath.Path, snapshot_dir: Optional[epath.Path] = None
) -> epath.Path:
  """Returns the snapshot directory from the step directory."""
  if snapshot_dir is None:
    snapshot_dir = step_dir.parent / _SNAPSHOTS
  new_path = snapshot_dir / step_dir.name
  return new_path

