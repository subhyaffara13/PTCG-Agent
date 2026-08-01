
def create_checkpoint_deleter(
    directory: epath.Path,
    *,
    name_format: step_lib.NameFormat[step_lib.Metadata],
    primary_host: Optional[int] = 0,
    todelete_subdir: Optional[str] = None,
    todelete_full_path: Optional[str] = None,
    enable_background_delete: bool = False,
    num_threads: Optional[int] = None,
) -> CheckpointDeleter:
  """Creates a CheckpointDeleter."""

  if enable_background_delete:
    return ThreadedCheckpointDeleter(
        directory,
        name_format=name_format,
        primary_host=primary_host,
        todelete_subdir=todelete_subdir,
        todelete_full_path=todelete_full_path,
        num_threads=num_threads,
    )
  else:
    return StandardCheckpointDeleter(
        directory,
        name_format=name_format,
        primary_host=primary_host,
        todelete_subdir=todelete_subdir,
        todelete_full_path=todelete_full_path,
        num_threads=num_threads,
    )

