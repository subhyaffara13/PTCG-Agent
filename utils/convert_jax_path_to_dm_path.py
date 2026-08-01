
def convert_jax_path_to_dm_path(
    jax_tree_path: Sequence[JaxKeyType],
) -> Tuple[Union[int, str, Hashable]]:
  """Converts a path from jax.tree_util to one from dm-tree."""

  # pytype:disable=attribute-error
  def _convert_key_fn(key: JaxKeyType) -> Union[int, str, Hashable]:
    if isinstance(key, (str, int)):
      return key  # int | str.
    if isinstance(key, jax.tree_util.SequenceKey):
      return key.idx  # int.
    if isinstance(key, jax.tree_util.DictKey):
      return key.key  # Hashable
    if isinstance(key, jax.tree_util.FlattenedIndexKey):
      return key.key  # int.
    if isinstance(key, jax.tree_util.GetAttrKey):
      return key.name  # str.
    raise ValueError(f"Jax tree key '{key}' of type '{type(key)}' not valid.")
  # pytype:enable=attribute-error

  return tuple(_convert_key_fn(key) for key in jax_tree_path)

