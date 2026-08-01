
def _get_backend_ocdbt_target_data_file_size(
    kvstore_spec: JsonSpec | None,
) -> int:
  """Gets OCDBT target data file size based on kvstore spec."""
  if kvstore_spec is None:
    return _DEFAULT_OCDBT_TARGET_DATA_FILE_SIZE
  base = kvstore_spec.get('base')

  if isinstance(base, str):
    # OCDBT base is generally a string when it's a GCS path.
    if gcs_utils.is_gcs_path(epath.Path(base)):
      return _GCS_OCDBT_TARGET_DATA_FILE_SIZE
  elif isinstance(base, dict):
    # OCDBT base can also be a dict with 'driver' and 'path' keys.
    if base.get('driver') in ('gcs', 'gcs_grpc'):
      return _GCS_OCDBT_TARGET_DATA_FILE_SIZE
    path_str = base.get('path')
    if path_str and gcs_utils.is_gcs_path(epath.Path(path_str)):
      return _GCS_OCDBT_TARGET_DATA_FILE_SIZE

  return _DEFAULT_OCDBT_TARGET_DATA_FILE_SIZE

