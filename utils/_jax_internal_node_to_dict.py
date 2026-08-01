
def _jax_internal_node_to_dict(node: Any) -> _FlattenedNode:
  """Converts JAX internal node to dict with clean keys and returns key mapping and tree_def."""
  keys_and_children, tree_def = utils.tree_flatten_with_path_one_level(node)
  original_key_by_clean_key = {}
  child_node_by_clean_key = {}
  for k, v in keys_and_children:
    clean_key = str(utils.get_key_name(k[0]))
    orig_key = jax.tree_util.keystr(k)
    original_key_by_clean_key[clean_key] = orig_key
    child_node_by_clean_key[clean_key] = v
  return _FlattenedNode(
      child_node_by_clean_key=child_node_by_clean_key,
      original_key_by_clean_key=original_key_by_clean_key,
      tree_def=tree_def,
  )

