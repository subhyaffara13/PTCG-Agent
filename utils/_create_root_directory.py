import logging
from typing import Optional

def _create_root_directory(
    directory: epath.PathLike,
    multiprocessing_options: MultiprocessingOptions,
    file_options: Optional[FileOptions] = None,
) -> None:
  """Creates the top-level directory if it does not already exist."""
  if multiprocessing_options.active_processes is not None:
    raise NotImplementedError(
        'Option `create=True` with `active_processes` set is not'
        ' supported. Please create the root directory yourself.'
    )
  directory = epath.Path(directory)
  if not directory.exists() and utils.is_primary_host(
      multiprocessing_options.primary_host
  ):
    # exists_ok=True is required, see b/362903314.
    directory.mkdir(
        parents=True,
        exist_ok=True,
        mode=file_options.path_permission_mode if file_options else None,
    )
    logging.info('Created directory=%s', directory)
  multihost.sync_global_processes(
      multihost.unique_barrier_key(
          'CheckpointManager:create_directory',
          prefix=multiprocessing_options.barrier_sync_key_prefix,
          # suffix=None,
      ),
      timeout=multihost.coordination_timeout(),
      processes=multiprocessing_options.active_processes,
  )

