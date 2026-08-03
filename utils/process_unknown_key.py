import logging
from typing import Any

def process_unknown_key(key: str, metadata_dict: dict[str, Any]) -> Any:
  if 'custom_metadata' in metadata_dict and metadata_dict['custom_metadata']:
    raise ValueError(
        'Provided metadata contains unknown key %s, and the custom_metadata'
        ' field is already defined.' % key
    )
  logging.warning(
      'Provided metadata contains unknown key %s. Adding it to'
      ' custom_metadata.',
      key,
  )
  return metadata_dict[key]

