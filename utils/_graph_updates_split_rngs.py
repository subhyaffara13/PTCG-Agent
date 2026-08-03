import random

def _graph_updates_split_rngs(
    node: tp.Any,
    /,
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
) -> SplitBackups:
  predicate = filterlib.to_predicate(only)
  backups: list[StreamBackup] = []
  for path, stream in graphlib.iter_graph(node, graph=True):
    if (
      isinstance(stream, RngStream)
      and predicate((*path, 'key'), stream.key)
      and predicate((*path, 'count'), stream.count)
    ):
      key = stream()
      backups.append((stream, stream.key[...], stream.count[...]))
      key = random.split(key, splits)
      if squeeze:
        key = key[0]
      stream.key.set_value(key)
      if squeeze:
        counts_shape = stream.count.shape
      elif isinstance(splits, int):
        counts_shape = (splits, *stream.count.shape)
      else:
        counts_shape = (*splits, *stream.count.shape)

      stream.count.set_value(jnp.zeros(counts_shape, dtype=jnp.uint32))

  return SplitBackups(backups)

