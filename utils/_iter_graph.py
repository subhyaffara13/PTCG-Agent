
def _iter_graph(node: tp.Any, /) -> tp.Iterator[tuple[PathParts, tp.Any]]:
  visited: set[int] = set()
  stack: list[tuple[PathParts, tp.Any, bool]] = [((), node, False)]
  while stack:
    path_parts, node, traversed = stack.pop(-1)
    if traversed or not (is_node(node) or isinstance(node, Variable)):
      yield path_parts, node
      continue

    if id(node) in visited:
      continue
    visited.add(id(node))

    if (node_impl := get_node_impl(node)) is None:
      yield path_parts, node
      continue

    stack.append((path_parts, node, True))
    for key, child in reversed(node_impl.node_dict(node).items()):
      stack.append(((*path_parts, key), child, False))

