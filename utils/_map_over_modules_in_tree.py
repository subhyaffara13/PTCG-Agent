
def _map_over_modules_in_tree(fn, tree_or_leaf):
  """Helper for mapping function over submodules."""
  dict_or_leaf = serialization.to_state_dict(tree_or_leaf)
  if not isinstance(dict_or_leaf, dict) or not dict_or_leaf:
    return fn('', tree_or_leaf)
  else:
    flat_dict = traverse_util.flatten_dict(dict_or_leaf, keep_empty_nodes=True)
    mapped_flat_dict = {
      k: fn('_' + '_'.join(k), v) for k, v in _sorted_items(flat_dict)
    }
    return serialization.from_state_dict(
      tree_or_leaf, traverse_util.unflatten_dict(mapped_flat_dict)
    )

