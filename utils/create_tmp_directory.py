import logging
import time
from typing import Optional, Set

def create_tmp_directory(
    tmp_dir: epath.Path,
    final_dir: epath.Path,
    *,
    primary_host: Optional[int] = 0,
    active_processes: Optional[Set[int]] = None,
    barrier_sync_key_prefix: Optional[str] = None,
    path_permission_mode: Optional[int] = None,
    metadata_store: Optional[checkpoint_metadata.MetadataStore] = None,
) -> epath.Path:
  """Creates a non-deterministic tmp directory for saving for given `final_dir`.

  Also writes checkpoint metadata in the tmp directory.

  Args:
    tmp_dir: The temporary directory path.
    final_dir: The eventual directory path where checkpoint will be committed.
    primary_host: primary host id, default=0.
    active_processes: Ids of active processes. default=None
    barrier_sync_key_prefix: A prefix to use for the barrier sync key.
    path_permission_mode: Path permission mode for the temp directory. e.g.
      0o750. Please check
      https://github.com/google/etils/blob/main/etils/epath/backend.py if your
        path is supported.
    metadata_store: optional `MetadataStore` instance. If present then it is
      used to create `StepMetadata` with current timestamp.

  Returns:
    The tmp directory.

  Raises:
    FileExistsError: if tmp directory already exists.
  """
  # Sync before existence is checked and directory is created because there are
  # additional existence checks happening in the callers of this function.
  multihost.sync_global_processes(
      multihost.unique_barrier_key(
          'create_tmp_directory:pre',
          prefix=barrier_sync_key_prefix,
          suffix=f'{final_dir.name}',
      ),
      timeout=multihost.coordination_timeout(),
      processes=active_processes,
  )
  if multihost.is_primary_host(primary_host):
    if tmp_dir.exists():
      if step_lib.is_path_temporary(tmp_dir):
        logging.warning(
            'Attempted to create temporary directory %s which already exists.'
            ' Removing existing directory since it is not finalized.',
            tmp_dir,
        )
        tmp_dir.rmtree()
      else:
        raise FileExistsError(
            f'Attempted to create temporary directory {tmp_dir} which already'
            ' exists but appears to be a finalized checkpoint.'
        )
    logging.info('Creating tmp directory %s', tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=False, mode=path_permission_mode)
    if metadata_store is not None:
      metadata = checkpoint_metadata.StepMetadata(
          init_timestamp_nsecs=time.time_ns(),
      )
      metadata_store.write(
          file_path=checkpoint_metadata.step_metadata_file_path(tmp_dir),
          metadata=step_metadata_serialization.serialize(metadata),
      )

  multihost.sync_global_processes(
      multihost.unique_barrier_key(
          'create_tmp_directory:post',
          prefix=barrier_sync_key_prefix,
          suffix=f'{final_dir.name}',
      ),
      timeout=multihost.coordination_timeout(),
      processes=active_processes,
  )
  return tmp_dir

