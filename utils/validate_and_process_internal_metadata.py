
def validate_and_process_internal_metadata(
    internal_metadata: Any,
) -> dict[str, Any]:
  """Validates and processes internal_metadata field."""
  if internal_metadata is None:
    return {}

  _validate_type(internal_metadata, dict)
  for k in internal_metadata:
    _validate_type(k, str)
  return internal_metadata

