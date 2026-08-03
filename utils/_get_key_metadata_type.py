from typing import Any

def _get_key_metadata_type(key: Any) -> KeyType:
  """Translates the JAX key class into a proto enum."""
  if tree_utils.is_sequence_key(key):
    return KeyType.SEQUENCE
  elif tree_utils.is_dict_key(key):
    return KeyType.DICT
  else:
    raise ValueError(f'Unsupported KeyEntry: {type(key)}: "{key}"')

