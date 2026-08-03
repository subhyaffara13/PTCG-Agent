from typing import Any

def get_json_tspec_write(
    info: types.ParamInfo,
    use_ocdbt: bool,
    global_shape: tuple[int, ...],
    local_shape: tuple[int, ...],
    dtype: jnp.dtype | np.dtype,
    process_index: int | str | None = None,
    metadata_key: str | None = None,
    arg: types.SaveArgs | None = None,
) -> dict[str, Any]:
  """Gets Tensorstore spec for writing."""
  tspec = _get_json_tspec(
      info,
      use_ocdbt=use_ocdbt,
      process_index=process_index,
      metadata_key=metadata_key,
  )

  chunk_byte_size = arg.chunk_byte_size if arg else None
  if use_ocdbt:
    ocdbt_target_data_file_size = info.ocdbt_target_data_file_size
    add_ocdbt_write_options(
        tspec['kvstore'],
        ocdbt_target_data_file_size,
    )
    chunk_byte_size = calculate_chunk_byte_size(
        local_shape,
        dtype,
        chunk_byte_size=chunk_byte_size,
        ocdbt_target_data_file_size=ocdbt_target_data_file_size,
        kvstore_spec=tspec['kvstore'],
    )

  chunk_shape = subchunking.choose_chunk_shape(
      global_shape,
      local_shape,
      dtype,
      chunk_byte_size,
  )

  tspec['metadata'] = build_zarr_shard_and_chunk_metadata(
      global_shape=global_shape,
      shard_shape=local_shape,
      use_compression=info.use_compression,
      use_zarr3=info.use_zarr3,
      chunk_shape=chunk_shape,
  )

  return tspec

