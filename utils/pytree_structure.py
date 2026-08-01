
def pytree_structure(directory: epath.PathLike) -> PyTree:
  """Reconstruct state dict from saved model format in `directory`."""
  directory = epath.Path(directory)
  jax.monitoring.record_event('/jax/orbax/deprecation/inferred_structure')

  def add_nested_key(subtree, nested_key, key_name):
    if not nested_key:
      return subtree

    current = nested_key[0]

    if len(nested_key) == 1:
      assert current not in subtree
      subtree[current] = leaf_placeholder(key_name)
      return subtree

    subkeys = nested_key[1:]
    if current not in subtree:
      subtree[current] = {}
    subtree[current] = add_nested_key(subtree[current], subkeys, key_name)
    return subtree

  keys = directory.iterdir()
  tree = {}
  for k in keys:
    # Sharding file stores sharding data that is only used by orbax. Therefore,
    # it shouldn't be included here. See b/279969796 for more details.
    if k.name == '_sharding':
      continue
    if k.name == '_METADATA':
      continue
    # array_metadatas is not a checkpoint param. Only used when ocdbt is used.
    # ocdbt is still disabled in some projects like paxml.
    if k.name == 'array_metadatas':
      continue
    tree = add_nested_key(tree, k.name.split('.'), k.name)
  return tree

