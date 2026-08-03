import os

def latest_checkpoint(
  ckpt_dir: str | os.PathLike, prefix: str = 'checkpoint_'
) -> str | None:
  """Retrieve the path of the latest checkpoint in a directory.

  Args:
    ckpt_dir: str: directory of checkpoints to restore from.
    prefix: str: name prefix of checkpoint files.

  Returns:
    The latest checkpoint path or None if no checkpoints were found.
  """
  checkpoint_files = _all_checkpoints(ckpt_dir, prefix)
  if checkpoint_files:
    return checkpoint_files[-1]
  else:
    return None

