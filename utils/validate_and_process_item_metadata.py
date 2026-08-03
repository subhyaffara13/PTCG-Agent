from typing import Any

def validate_and_process_item_metadata(
    item_metadata: Any,
) -> CompositeItemMetadata | SingleItemMetadata | None:
  """Validates and processes item_metadata field."""
  if item_metadata is None:
    return None

  if isinstance(item_metadata, CompositeItemMetadata):
    for k in item_metadata:
      _validate_type(k, str)
    return item_metadata
  else:
    return item_metadata

