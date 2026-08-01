
def _get_json_tspec(
    info: types.ParamInfo,
    use_ocdbt: bool,
    *,
    process_index: int | str | None = None,
    metadata_key: str | None = None,
    raise_array_data_missing_error: bool = True,
) -> dict[str, Any]:
  """Gets Tensorstore spec in JSON format."""
  if info.name is None or info.parent_dir is None:
    raise ValueError('Must provide info.name and info.parent_dir.')
  parent_dir = info.parent_dir
  assert parent_dir is not None
  directory = parent_dir.as_posix()
  kvstore_tspec = build_kvstore_tspec(
      directory,
      name=info.name,
      use_ocdbt=use_ocdbt,
      process_id=process_index,
  )

  tspec = {
      'driver': ZARR_VER3 if info.use_zarr3 else ZARR_VER2,
      'kvstore': kvstore_tspec,
      'recheck_cached_data': False,
      'recheck_cached_metadata': False,
      # Raise error if data is missing.
      'fill_missing_data_reads': not raise_array_data_missing_error,
  }
  if metadata_key is not None:
    tspec['metadata_key'] = metadata_key
  return tspec

