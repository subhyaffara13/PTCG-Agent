from typing import Any

def build_array_write_spec(
    info: types.ParamInfo,
    arg: types.SaveArgs | None = None,
    *,
    global_shape: arrays_types.Shape,
    local_shape: arrays_types.Shape,
    dtype: jnp.dtype | np.dtype,
    use_ocdbt: bool,
    process_index: int | str | None = None,
    replica_separate_folder: bool = False,
    metadata_key: str | None = None,
    ext_metadata: dict[str, Any] | None = None,
) -> ArrayWriteSpec:
  """Gets ArrayWriteSpec for writing."""
  if info.name is None or info.parent_dir is None:
    raise ValueError('Must provide info.name and info.parent_dir.')
  parent_dir = info.parent_dir
  assert parent_dir is not None
  directory = parent_dir.as_posix()

  return ArrayWriteSpec(
      directory,
      relative_array_filename=info.name,
      global_shape=global_shape,
      write_shape=local_shape,
      dtype=dtype,
      target_dtype=(arg.dtype if arg is not None else None),
      chunk_byte_size=(arg.chunk_byte_size if arg is not None else None),
      shard_axes=(arg.shard_axes if arg is not None else tuple()),
      use_compression=info.use_compression,
      use_zarr3=info.use_zarr3,
      use_ocdbt=use_ocdbt,
      process_id=process_index,
      replica_separate_folder=replica_separate_folder,
      ocdbt_target_data_file_size=info.ocdbt_target_data_file_size,
      metadata_key=metadata_key,
      ext_metadata=ext_metadata,
  )

