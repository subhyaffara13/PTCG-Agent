
def deserialize_tree(
    serialized: PyTree, target: PyTree, keep_empty_nodes: bool = False
) -> PyTree:
  """Deserializes a PyTree to the same structure as `target`."""
  def _reconstruct_from_keypath(keypath, _):
    result = serialized
    for key in keypath:
      if type(result) in (dict, list, tuple):
        key_name = get_key_name(key)
        if isinstance(result, dict) and key_name not in result:
          key_name = str(key_name)
        result = result[key_name]
      else:
        result = look_up_pytree_key(result, key)
    return result

  return jax.tree_util.tree_map_with_path(
      _reconstruct_from_keypath,
      target,
      is_leaf=is_empty_or_leaf if keep_empty_nodes else None,
  )

