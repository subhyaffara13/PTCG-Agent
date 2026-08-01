
def get_col_name(keypath: tp.Sequence[Any]) -> str:
  """Given the keypath of a Flax variable type, return its Linen collection name."""
  # Infer variable type from the leaf's path, which contains its Linen collection name
  assert isinstance(keypath[0], jax.tree_util.DictKey)
  return str(keypath[0].key)

