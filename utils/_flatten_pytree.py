
def _flatten_pytree(pytree: tp.Any):
  leaves, treedef = jax.tree_util.tree_flatten_with_path(
    pytree, is_leaf=lambda x: x is not pytree
  )
  nodes = [(_key_path_to_key(path[0]), value) for path, value in leaves]
  key_index = HashableMapping(
    {key: i for i, (key, _) in enumerate(nodes)}, copy=False
  )
  # Sort by key to match the path-sorted order used by _merge_to_flat_state.
  # key_index records the original jax tree_flatten order so _unflatten_pytree
  # can restore it before calling treedef.unflatten.
  nodes.sort()
  return nodes, IndexesPytreeDef(key_index, treedef)

