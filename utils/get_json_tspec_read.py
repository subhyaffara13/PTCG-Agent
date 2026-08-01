
def get_json_tspec_read(
    info: types.ParamInfo,
    use_ocdbt: bool,
    metadata_key: str | None = None,
    raise_array_data_missing_error: bool = True,
) -> dict[str, Any]:
  """Gets Tensorstore spec for reading."""
  return _get_json_tspec(
      info,
      use_ocdbt=use_ocdbt,
      metadata_key=metadata_key,
      raise_array_data_missing_error=raise_array_data_missing_error,
  )

