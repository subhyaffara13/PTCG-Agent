
def detect_process_index(directory: epath.Path, step: int) -> int | None:
  """Inspects the disk to find which process index created this step."""
  step_path = directory / str(step)
  if not step_path.exists():
    return None

  # Check for standard Orbax/OCDBT structure
  # P2P checkpoint requires 'state' item in CompositeArgs
  try:
    item_path = step_path / constants.STATE_SUBDIR
    if item_path.exists():
      for path in item_path.glob(f'{constants.PROCESS_SUBDIR_PREFIX}*'):
        if path.is_dir():
          # Format: ocdbt.process_0, ocdbt.process_12, etc.
          return int(path.name.split('_')[-1])
  except (ValueError, IndexError, OSError) as e:
    logging.warning('Could not detect process index for step %d: %s', step, e)

  return None

