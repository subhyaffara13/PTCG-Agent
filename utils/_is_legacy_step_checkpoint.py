
def _is_legacy_step_checkpoint(path: epath.Path) -> bool:
  """Determines if the path resembles an Orbax step directory.

  Note that this is not foolproof, and users should not add extra files to the
  checkpoint directory beyond what is done by CheckpointManager.

  Args:
    path: path to check.

  Returns:
    bool indicating whether the path resembles an Orbax step directory.
  """
  name = path.name
  # Path must be a directory and either a digit, or end in '_' + digit.
  return path.is_dir() and (name.isdigit() or name.split('_')[-1].isdigit())

