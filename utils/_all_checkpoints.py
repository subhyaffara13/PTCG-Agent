import os
import pathlib
from typing import Any

def _all_checkpoints(
  ckpt_dir: str | os.PathLike, prefix: str = 'checkpoint_'
) -> list[str]:
  """Retrieve all checkpoint paths in directory.

  Args:
    ckpt_dir: str: directory of checkpoints to restore from.
    prefix: str: name prefix of checkpoint files.

  Returns:
    Sorted list of checkpoint paths or empty list if no checkpoints were found.
  """
  ckpt_dir = os.fspath(ckpt_dir)  # Pathlib -> str
  checkpoint_files: list[Any] = [
    pathlib.PurePath(c) for c in _allowempty_listdir(ckpt_dir)
  ]
  checkpoint_files = [
    os.path.join(ckpt_dir, c)
    for c in checkpoint_files
    if c.match(f'{prefix}*')
    and not c.match(f'{prefix}tmp')
    and not c.match(f'*{MP_ARRAY_POSTFIX}')
    and not c.match(f'*{ocp.utils.TMP_DIR_SUFFIX}*')
  ]
  checkpoint_files = natural_sort(checkpoint_files)
  if checkpoint_files:
    return checkpoint_files
  else:
    return []

