import os

def available_steps(
  ckpt_dir: str | os.PathLike,
  prefix: str = 'checkpoint_',
  step_type: type = int,
) -> list[int | float]:
  """Return step numbers of available checkpoints in a directory.


  Args:
    ckpt_dir: str: directory of checkpoints to restore from.
    prefix: str: name prefix of checkpoint files.
    step_type: type: type for steps, int (default) or float.

  Returns:
    Sorted list of available steps or empty list if no checkpoints were found.
  """
  checkpoint_files = _all_checkpoints(ckpt_dir, prefix)

  checkpoint_steps = []

  for file in checkpoint_files:
    prefix_idx = file.rfind(prefix)
    checkpoint_steps += [step_type(file[prefix_idx + len(prefix) :])]

  return checkpoint_steps

