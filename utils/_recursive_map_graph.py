
def _recursive_map_graph(
    f: tp.Callable[[PathParts, tp.Any], tp.Any],
    node: tp.Any,
    path: PathParts,
    visited: set[int],
    results: dict[int, tp.Any],
) -> tp.Any:
  node_id = id(node)
  if node_id in visited:
    if node_id in results:
      return results[node_id]
    path_str = '/'.join(builtins.map(str, path))
    raise ValueError(
        f"Found cycle in the graph at path '{path_str}'. Node of type"
        f' {type(node)} has already been visited but has not been returned yet.'
    )
  node_impl = get_node_impl(node)
  if (
      type(node_impl) is GraphNodeImpl
      or isinstance(node, Variable)
      or is_array_ref(node)
  ):
    visited.add(node_id)
  if node_impl is not None:
    for key, value in node_impl.node_dict(node).items():
      new_value = _recursive_map_graph(f, value, (*path, key), visited, results)
      if new_value is not value:
        if node_impl.set_key is not None and value is not new_value:
          node_impl.set_key(node, key, new_value)
        else:
          raise ValueError(
              f"Cannot update key '{key}' for node of type '{type(node)}'"
              ' because the node does not support mutation.'
          )

  new_node = f(path, node)
  results[node_id] = new_node
  return new_node

