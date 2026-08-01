
def _node_paths(
  node: tp.Any,
  node_paths: dict[int, list[PathParts]],
  path: PathParts,
  duplicate_candidate: filterlib.Predicate,
  /,
):
  _is_graph_node = is_graph_node(node)
  _is_pytree_node = is_pytree_node(node)
  _is_node_leaf = is_node_leaf(node)

  if _is_graph_node or _is_pytree_node or _is_node_leaf:
    node_id = id(node)
    if node_id in node_paths:
      if (_is_graph_node or _is_node_leaf) and duplicate_candidate(path, node):
        node_paths[node_id].append(path)
      return
    if _is_graph_node or _is_node_leaf:
      node_paths[node_id] = [path]
    node_impl = get_node_impl(node)
    if node_impl is None:
      return
    node_dict = node_impl.node_dict(node)
    for key, value in node_dict.items():
      _node_paths(value, node_paths, (*path, key), duplicate_candidate)

