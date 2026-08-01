
def _safe_flatten_dict(dct: dict[Any, Any]
                       ) -> tuple[list[Any], tree_util.PyTreeDef]:
  # We avoid comparison between keys by just using the original order
  keys, values = [], []
  for key, value in dct.items():
    try:
      tree_util.tree_leaves(value)
    except:
      # If flattening fails, we substitute a sentinel object.
      value = cant_flatten
    keys.append(key)
    values.append(value)
  return tree_util.tree_flatten(_DictWrapper(keys, values))

