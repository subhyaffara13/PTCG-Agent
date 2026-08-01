
def _simple_fork_rngs(
    node: tp.Any,
    /,
    *,
    predicate_splits: tp.Mapping[tp.Callable, tp.Any],
    graph: bool,
) -> tp.Any:
  def _fork_stream(path, node):
    if isinstance(node, RngStream):
      for predicate, splits in predicate_splits.items():
        if predicate((*path, 'key'), node.key) and predicate(
            (*path, 'count'), node.count
        ):
          return node.fork(split=splits)
    return node

  return graphlib.recursive_map(_fork_stream, node, graph=graph)

