from typing import Any

def validate_and_process_custom_metadata(
    custom_metadata: Any,
) -> dict[str, Any]:
  """Validates and processes custom field."""
  if custom_metadata is None:
    return {}

  _validate_type(custom_metadata, dict)
  for k in custom_metadata:
    _validate_type(k, str)
  return custom_metadata

