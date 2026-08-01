
def _keypath_from_key_type(key_name: str, key_type: KeyType) -> Any:
  """Converts from Key in InternalTreeMetadata to JAX keypath class."""
  if key_type == KeyType.SEQUENCE:
    return jax.tree_util.SequenceKey(int(key_name))
  elif key_type == KeyType.DICT:
    return jax.tree_util.DictKey(key_name)
  else:
    raise ValueError(f'Unsupported KeyEntry: {key_type}')

