
def is_orbax_checkpoint(path: epath.PathLike) -> bool:
  """Returns whether the path is LIKELY an Orbax checkpoint.

  It is always possible to assemble files within a directory to look like an
  Orbax checkpoint, even if loading would later reject it as invalid. This
  function provides an easy heuristic as to what constitutes an Orbax
  checkpoint.

  Furthermore, Orbax provides a high degree of customizability, so many
  customized edge cases are possible that would not be detected by this
  function. However, most standard use cases should be covered.

  IMPORTANT: The function is unlikely to return a false positive (True when the
  checkpoint is NOT an Orbax checkpoint), but is more likely to return a
  false negative (False when the checkpoint IS an Orbax checkpoint).

  The function is expected to return True when the directory points to a step
  directory (saved by `CheckpointManager`) or an item directory (saved by
  `PyTreeCheckpointHandler`). It will return False when pointing to a root
  directory (containing multiple step directories).


  Args:
    path: A directory corresponding to an Orbax checkpoint.

  Returns:
    True if the path is LIKELY an Orbax checkpoint.

  Raises:
    FileNotFoundError: If the path does not exist.
    NotADirectoryError: If the path is not a directory.
  """
  path = epath.Path(path)
  if not path.exists():
    raise FileNotFoundError(f'Checkpoint path {path} does not exist.')
  if not path.is_dir():
    raise NotADirectoryError(f'Checkpoint path {path} is not a directory.')
  metadata_store = checkpoint_metadata.metadata_store(enable_write=False)
  # Path points to a single step checkpoint with valid metadata.
  if (
      metadata_store.read(checkpoint_metadata.step_metadata_file_path(path))
      is not None
  ):
    return True

  # Path points to valid PyTree checkpoint without newer metadata.
  if is_pytree_checkpoint(path):
    return True

  # Path points to a root directory containing a valid PyTree checkpoint.
  if any([is_pytree_checkpoint(p) for p in path.iterdir()]):
    return True

  return False


def is_orbax_checkpoint(path: path_types.PathLike) -> bool:
  """Returns True if the path is an Orbax checkpoint."""
  return asyncio_utils.run_sync(_is_orbax_checkpoint_async(path))

