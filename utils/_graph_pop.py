
def _graph_pop(
  node: tp.Any,
  id_to_index: dict[int, Index],
  path_parts: PathParts,
  flat_states: tuple[dict[PathParts, LeafType], ...],
  predicates: tuple[filterlib.Predicate, ...],
) -> None:
  if not is_node(node):
    raise RuntimeError(f'Unsupported type: {type(node)}, this is a bug.')

  if id(node) in id_to_index:
    return

  id_to_index[id(node)] = len(id_to_index)
  node_impl = get_node_impl(node)
  if node_impl is None:
    raise TypeError(f'Unknown node type: {type(node)}')
  node_dict = node_impl.node_dict(node)

  for name, value in node_dict.items():
    if is_node(value):
      _graph_pop(
        node=value,
        id_to_index=id_to_index,
        path_parts=(*path_parts, name),
        flat_states=flat_states,
        predicates=predicates,
      )
      continue
    elif not is_node_leaf(value):
      continue
    elif id(value) in id_to_index:
      continue

    node_path = (*path_parts, name)
    node_impl = get_node_impl(node)
    if node_impl is None:
      raise TypeError(f'Unknown node type: {type(node)}')

    for state, predicate in zip(flat_states, predicates):
      if predicate(node_path, value):
        if node_impl.pop_key is None:
          raise ValueError(
            f'Cannot pop key {name!r} from node of type {type(node).__name__}'
          )
        id_to_index[id(value)] = len(id_to_index)
        node_impl.pop_key(node, name)
        if isinstance(value, Variable):
          value = value
        state[node_path] = value  # type: ignore[index] # mypy is wrong here?
        break
    else:
      # NOTE: should we raise an error here?
      pass

