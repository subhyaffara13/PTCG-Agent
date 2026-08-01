
def get_d_files_mtimes(path: path_types.Path) -> list[int]:
  """Gets a list of last modified times for d files in a PyTree checkpoint.

  Assumes a structure like::

    path/
      <STATE_CHECKPOINTABLE_KEY>/
        ocdbt.process_0/
          d/
            <d_file_1>
            ...
            <d_file_n>
        ocdbt.process_1/
          ...

  The `path` and immediate subdirectories may optionally contain tmp suffixes.

  Args:
    path: The path to the checkpoint directory.

  Returns:
    A list of last modified times for d files in the checkpoint.
  """
  mtimes = []
  matching_dirs = list(path.parent.glob(f'{path.name}*'))
  if not matching_dirs:
    # Temp path not created yet.
    return []
  assert (
      len(matching_dirs) == 1
  ), f'Expected exactly one matching directory, got {matching_dirs}.'
  tmpdir = matching_dirs[0]
  matching_pytree_dirs = list(tmpdir.glob(f'{STATE_CHECKPOINTABLE_KEY}*'))
  if not matching_pytree_dirs:
    # Temp path not created yet.
    return []
  assert len(matching_pytree_dirs) == 1, (
      'Expected exactly one matching pytree directory, got'
      f' {matching_pytree_dirs}.'
  )
  pytree_dir = matching_pytree_dirs[0]
  for idx in range(multihost.process_count()):
    d_path = pytree_dir / f'ocdbt.process_{idx}' / 'd'
    if not d_path.exists():
      continue
    for f in d_path.iterdir():
      # TensorStore tmp files can get deleted while iterating. We try to be
      # resilient to this.
      try:
        mtimes.append(f.stat().mtime)
      except OSError:
        pass
  return mtimes

