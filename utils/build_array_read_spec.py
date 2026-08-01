
def build_array_read_spec(
    info: types.ParamInfo,
    *,
    use_ocdbt: bool,
    metadata_key: str | None = None,
    raise_array_data_missing_error: bool = True,
    target_dtype: DType | None = None,
) -> ArrayReadSpec:
  """Gets ArrayReadSpec for reading."""
  if info.name is None or info.parent_dir is None:
    raise ValueError('Must provide info.name and info.parent_dir.')
  return ArrayReadSpec(
      directory=info.parent_dir.as_posix(),
      relative_array_filename=info.name,
      use_zarr3=info.use_zarr3,
      use_ocdbt=use_ocdbt,
      metadata_key=metadata_key,
      raise_array_data_missing_error=raise_array_data_missing_error,
      target_dtype=target_dtype,
  )

