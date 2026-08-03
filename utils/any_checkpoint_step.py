from typing import Optional

def any_checkpoint_step(checkpoint_dir: epath.PathLike) -> Optional[int]:
  """Returns any finalized checkpoint step in the directory or None.

  This avoids iterating over the entire directory.

  Args:
    checkpoint_dir: Checkpoint directory.

  Returns:
    Any finalized checkpoint step in the directory or None.
  """
  checkpoint_dir = epath.Path(checkpoint_dir)
  for s in checkpoint_dir.iterdir():
    if _is_legacy_finalized_step_checkpoint(s):
      return step_from_checkpoint_name(s.name)
  return None

