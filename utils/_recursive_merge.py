
def _recursive_merge(
    t1: Any,
    t2: Any,
    overwrite: bool,
    is_leaf: Callable[[Any], bool],
) -> Any:
  """Recursively merges t1 into t2 with structure-aware logic."""
  if type(t1) is not type(t2) and not overwrite:
    raise ValueError(f'Types do not match: {type(t1)} and {type(t2)}')

  if is_leaf(t1) or is_leaf(t2):
    return t1 if t1 is not None else t2

  node_type = type(t1)

  if isinstance(t1, abc.Mapping) or utils.isinstance_of_namedtuple(t1):
    t1_dict = t1._asdict() if utils.isinstance_of_namedtuple(t1) else t1
    t2_dict = t2._asdict() if utils.isinstance_of_namedtuple(t2) else t2
    merged = dict(t2_dict)
    for k, v1 in t1_dict.items():
      if k in t2_dict:
        merged[k] = _recursive_merge(v1, t2_dict[k], overwrite, is_leaf)
      else:
        merged[k] = v1
    try:
      if utils.isinstance_of_namedtuple(t1):
        return node_type(**merged)
      return node_type(merged)
    except (TypeError, ValueError):
      return merged

  if isinstance(t1, abc.Sequence) and not isinstance(t1, str):
    if len(t1) != len(t2):
      raise ValueError(
          f'Sequence lengths do not match: {len(t1)} and {len(t2)}'
      )
    merged = [
        _recursive_merge(e1, e2, overwrite, is_leaf) for e1, e2 in zip(t1, t2)
    ]
    try:
      return node_type(merged)
    except (TypeError, ValueError):
      return merged

  if utils.is_jax_internal_node(t1):
    t1_flat = _jax_internal_node_to_dict(t1)
    t2_flat = _jax_internal_node_to_dict(t2)

    merged_children_dict = _recursive_merge(
        t1_flat.child_node_by_clean_key,
        t2_flat.child_node_by_clean_key,
        overwrite,
        is_leaf,
    )

    children = [
        merged_children_dict[k] for k in t1_flat.child_node_by_clean_key.keys()
    ]
    return jax.tree_util.tree_unflatten(t1_flat.tree_def, children)

  return t1


def _recursive_merge(dict1, dict2):
  """Recursively merge two dicts."""
  flat_map = traversals.flatten_mapping(dict1)
  flat_map |= traversals.flatten_mapping(dict2)
  return traversals.unflatten_mapping(flat_map)

