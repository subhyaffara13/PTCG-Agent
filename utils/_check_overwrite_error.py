import os
import pathlib
from typing import Any

def _check_overwrite_error(
  ckpt_tmp_path: str, ckpt_path: str, base_path: str, step: int
):
  """Throw error if a ckpt file of this step or higher already exists."""
  dir_path, prefix = os.path.split(base_path)
  checkpoint_files: list[Any] = [
    pathlib.PurePath(c) for c in _allowempty_listdir(dir_path)
  ]
  checkpoint_files = [
    os.path.join(dir_path, c)
    for c in checkpoint_files
    if c.match(f'{prefix}*') and not c.match(f'*{MP_ARRAY_POSTFIX}')
  ]
  if ckpt_path in checkpoint_files:
    raise errors.InvalidCheckpointError(ckpt_path, step)
  checkpoint_files.append(ckpt_path)

  checkpoint_files = natural_sort(checkpoint_files)
  # Handle the case if the job was preempted after the temporary checkpoint
  # was written, but before it was renamed to the final checkpoint name
  if checkpoint_files[-1] == ckpt_tmp_path:
    checkpoint_files.pop()
  if ckpt_path != checkpoint_files[-1]:
    raise errors.InvalidCheckpointError(ckpt_path, step)

