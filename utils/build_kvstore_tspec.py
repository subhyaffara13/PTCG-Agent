import logging
import os
import re

def build_kvstore_tspec(
    directory: str,
    name: str | None = None,
    *,
    use_ocdbt: bool = True,
    process_id: int | str | None = None,
    replica_separate_folder: bool = False,
) -> JsonSpec:
  """Constructs a spec for a Tensorstore KvStore.

  Args:
    directory: Base path (key prefix) of the KvStore, used by the underlying
      file driver.
    name: Name (filename) of the parameter.
    use_ocdbt: Whether to use OCDBT driver.
    process_id: [only used with OCDBT driver] If provided,
      `{directory}/ocdbt.process_{process_id}` path is used as the base path. If
      a string, must conform to [A-Za-z0-9]+ pattern.
    replica_separate_folder: Whether a replica separated folder is used.

  Returns:
    A Tensorstore KvStore spec in dictionary form.
  """
  default_driver = DEFAULT_DRIVER
  # Normalize path to exclude trailing '/'. In GCS path case, we will need to
  # fix the path prefix to add back the stripped '/'.
  directory = os.path.normpath(directory).replace('gs:/', 'gs://')
  is_gcs_path = directory.startswith('gs://')

  if use_ocdbt:
    if not is_gcs_path and not os.path.isabs(directory):
      raise ValueError(f'Checkpoint path should be absolute. Got {directory}')
    if process_id is not None:
      process_id = str(process_id)
      if re.fullmatch(_OCDBT_PROCESS_ID_RE, process_id) is None:
        raise ValueError(
            f'process_id must conform to {_OCDBT_PROCESS_ID_RE} pattern'
            f', got {process_id}'
        )

      join_paths = [directory, f'{PROCESS_SUBDIR_PREFIX}{process_id}']
      if replica_separate_folder:
        # make sure the the sub dictory is ended with '_process_id'
        join_paths = [
            directory,
            f'{PROCESS_SUBDIR_PREFIX}{REPLICA_SUBDIR_SUFFIX}{process_id}',
        ]
      directory = os.path.join(*join_paths)
    # Base KVStore spec (nested within OCDBT KVStore spec).
    if is_gcs_path:
      base_driver_spec = _get_kvstore_for_gcs(directory)
    else:
      base_driver_spec = {'driver': default_driver, 'path': str(directory)}
    # For OCDBT on local filesystems (including GCSFuse), we can safely use
    # non-atomic writes for data files to avoid expensive renames. However,
    # the manifest file still requires atomic writes to avoid corruption.
    # We achieve this by splitting the spec into 'base' (for data files) and
    # 'manifest'.
    try:
      resolved_base_spec = ts.KvStore.Spec(base_driver_spec).to_json()
    except Exception:  # pylint: disable=broad-except
      logging.warning(
          'Failed to resolve base spec %r, falling back to default.',
          base_driver_spec,
          exc_info=True,
      )
      resolved_base_spec = base_driver_spec

    if (
        isinstance(resolved_base_spec, dict)
        and resolved_base_spec.get('driver') == 'file'
    ):
      kv_spec = {
          'driver': 'ocdbt',
          'base': {
              **resolved_base_spec,
              'file_io_locking': {'mode': 'non_atomic'},
          },
          'manifest': base_driver_spec,
      }
    else:
      kv_spec = {
          'driver': 'ocdbt',
          'base': base_driver_spec,
      }

    if name is not None:
      kv_spec['path'] = name

    kv_spec.update({  # pytype: disable=attribute-error
        # References the cache specified in ts.Context.
        'cache_pool': 'cache_pool#ocdbt',
    })

    if is_remote_storage(kv_spec):
      kv_spec.update({  # pytype: disable=attribute-error
          # Enable read coalescing.  This feature merges adjacent read_ops into
          # one, which could reduce I/O ops by a factor of 10. This is
          # especially beneficial for unstacked models.
          'experimental_read_coalescing_threshold_bytes': 1000000,
          'experimental_read_coalescing_merged_bytes': 500000000000,
          'experimental_read_coalescing_interval': '1ms',
      })
  else:
    if name is None:
      path = directory
    else:
      path = os.path.join(directory, name)
    if is_gcs_path:
      kv_spec = _get_kvstore_for_gcs(path)
    else:
      kv_spec = {'driver': default_driver, 'path': path}

  return kv_spec

