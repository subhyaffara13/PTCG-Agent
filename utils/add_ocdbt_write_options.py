
def add_ocdbt_write_options(
    kvstore_tspec: JsonSpec,
    target_data_file_size: int | None = None,
) -> None:
  """Adds write-specific options to a TensorStore OCDBT KVStore spec."""
  if target_data_file_size is None:
    target_data_file_size = _get_backend_ocdbt_target_data_file_size(
        kvstore_tspec
    )
  # TODO: b/354139177 - Disallow too small values, too.
  if target_data_file_size < 0:
    raise ValueError(
        'OCDBT target_data_file_size must be >= 0, where 0 means no limit'
        f'; got {target_data_file_size}'
    )
  kvstore_tspec['target_data_file_size'] = target_data_file_size

  kvstore_tspec['config'] = {
      # Store .zarray metadata inline but not large chunks.
      'max_inline_value_bytes': 1024,
      # Large value allows a single root node to support faster traversal.
      'max_decoded_node_bytes': 100000000,
      # There won't be any concurrent writes by multiple machines to the same
      # OCDBT database.  Therefore, we can use the simpler and more efficient
      # single-file manifest format in all cases.
      'manifest_kind': 'single',
  }
  # assume_config avoids writing an initial empty manifest to ensure a
  # consistent configuration, since Orbax never writes to the same OCDBT
  # database concurrently from multiple processes.
  kvstore_tspec.update(assume_config=True)

