
def _iter_tree(node: tp.Any, /) -> tp.Iterator[tuple[PathParts, tp.Any]]:
  in_progress: dict[int, str] = {}
  seen_refs: dict[int, str] = {}
  stack: list[tuple[PathParts, tp.Any, bool]] = [((), node, False)]
  while stack:
    path, current, traversed = stack.pop()

    if traversed:
      in_progress.pop(id(current), None)
      yield path, current
      continue

    if not is_pytree_node(current, check_graph_registry=False):
      _check_valid_pytree(current, 'iter_graph', '/'.join(builtins.map(str, path)))
      if isinstance(current, Variable) or variablelib.is_array_ref(current):
        obj_id = id(current)
        str_path = '/'.join(builtins.map(str, path))
        if obj_id in seen_refs:
          raise ValueError(
            f'Duplicate {current}\nfound at paths:\n\n'
            f'  - {seen_refs[obj_id]}\n'
            f'  - {str_path}\n\n'
            'Tree mode (graph=False) does not support shared references. '
            + _tree_mode_suggestion_api('iter_graph')
          )
        seen_refs[obj_id] = str_path
      yield path, current
      continue

    obj_id = id(current)
    str_path = '/'.join(builtins.map(str, path))
    if obj_id in in_progress:
      raise ValueError(
        f'Cycle detected for {type(current).__name__}\nfound at paths:\n\n'
        f'  - {in_progress[obj_id]}\n'
        f'  - {str_path}\n\n'
        'Cycles are not supported with graph=False. '
        + _tree_mode_suggestion_api('iter_graph')
      )
    in_progress[obj_id] = str_path

    stack.append((path, current, True))
    children, _ = jax.tree_util.tree_flatten_with_path(
      current, is_leaf=lambda x: x is not current
    )
    for jax_key_path, child in reversed(children):
      key = _key_path_to_key(jax_key_path[0])
      stack.append(((*path, key), child, False))

