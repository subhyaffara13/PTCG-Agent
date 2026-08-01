
def _recursive_map_tree(
    f: tp.Callable[[PathParts, tp.Any], tp.Any],
    node: tp.Any,
) -> tp.Any:
  in_progress: dict[int, str] = {}
  seen_refs: dict[int, str] = {}

  def _recurse(path: PathParts, current: tp.Any) -> tp.Any:
    if not is_pytree_node(current, check_graph_registry=False):
      _check_valid_pytree(current, 'recursive_map', '/'.join(builtins.map(str, path)))
      if isinstance(current, Variable) or is_array_ref(current):
        obj_id = id(current)
        str_path = '/'.join(builtins.map(str, path))
        if obj_id in seen_refs:
          raise ValueError(
            f'Duplicate {current}\nfound at paths:\n\n'
            f'  - {seen_refs[obj_id]}\n'
            f'  - {str_path}\n\n'
            'Tree mode (graph=False) does not support shared references. '
            + _tree_mode_suggestion_api('recursive_map')
          )
        seen_refs[obj_id] = str_path
      return f(path, current)

    obj_id = id(current)
    str_path = '/'.join(builtins.map(str, path))
    if obj_id in in_progress:
      raise ValueError(
        f'Cycle detected for {type(current).__name__}\nfound at paths:\n\n'
        f'  - {in_progress[obj_id]}\n'
        f'  - {str_path}\n\n'
        'Cycles are not supported with graph=False. '
        + _tree_mode_suggestion_api('recursive_map')
      )
    in_progress[obj_id] = str_path

    children_with_path, treedef = jax.tree_util.tree_flatten_with_path(
      current, is_leaf=lambda x: x is not current
    )
    new_children = []
    for jax_key_path, child in children_with_path:
      key = _key_path_to_key(jax_key_path[0])
      new_child = _recurse((*path, key), child)
      new_children.append(new_child)

    new_node = treedef.unflatten(new_children)
    result = f(path, new_node)

    in_progress.pop(obj_id, None)
    return result

  return _recurse((), node)

