from typing import Union

def _get_key(key: _KeyEntry) -> Union[int, str]:
  """Convert a ``KeyEntry``` to a usual type."""
  if isinstance(key, jax.tree_util.DictKey):
    if isinstance(key.key, (str, int)):
      return key.key
    raise KeyError("Hashable keys not supported")
  # pylint: disable=attribute-error
  if isinstance(key, jax.tree_util.FlattenedIndexKey):
    return key.key  # int.
  if isinstance(key, jax.tree_util.GetAttrKey):
    return key.name  # str.
  if isinstance(key, jax.tree_util.SequenceKey):
    return key.idx  # int.
  if isinstance(key, NamedTupleKey):
    return key.name  # str.
  # pylint: enable=attribute-error
  raise KeyError(f"Tree key '{key}' of type '{type(key)}' not valid.")


def _get_key(key: int):
  return f'tensorstore_checkpoint_{key}'

