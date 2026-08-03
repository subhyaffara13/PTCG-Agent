from typing import Any

def _get_suffix_value_pairs(
  tree_or_leaf: Any,
) -> list[tuple[str, type['Module']]]:
  """Helper for naming pytrees of submodules."""
  dict_or_leaf = serialization.to_state_dict(tree_or_leaf)
  if not isinstance(dict_or_leaf, dict) or not dict_or_leaf:
    return [('', tree_or_leaf)]
  else:
    flat_dict = traverse_util.flatten_dict(dict_or_leaf)
    return [('_' + '_'.join(k), v) for k, v in _sorted_items(flat_dict)]

