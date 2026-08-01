
def _graph_updates_fork_rngs(
    node: tp.Any,
    /,
    *,
    predicate_splits: tp.Mapping[tp.Callable, tp.Any],
    graph: bool,
) -> SplitBackups:
  backups: list[StreamBackup] = []
  for path, stream in graphlib.iter_graph(node, graph=graph):
    for predicate, splits in predicate_splits.items():
      if (
          isinstance(stream, RngStream)
          and predicate((*path, 'key'), stream.key)
          and predicate((*path, 'count'), stream.count)
      ):
        forked_stream = stream.fork(split=splits)
        # backup the original stream state
        backups.append((stream, stream.key[...], stream.count[...]))
        # apply the forked key and count to the original stream
        stream.key.set_value(forked_stream.key.get_value())
        stream.count.set_value(forked_stream.count.get_value())

  return SplitBackups(backups)

