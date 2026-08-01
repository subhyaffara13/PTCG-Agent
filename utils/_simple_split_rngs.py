
def _simple_split_rngs(
    node: tp.Any,
    /,
    *,
    splits: int | tuple[int, ...],
    only: filterlib.Filter = ...,
    squeeze: bool = False,
    graph: bool,
) -> tp.Any:
  predicate = filterlib.to_predicate(only)

  def _split_stream(path, node):
    if (
      isinstance(node, RngStream)
      and predicate((*path, 'key'), node.key)
      and predicate((*path, 'count'), node.count)
    ):
      key = random.split(node(), splits)
      if squeeze:
        key = key[0]
      if squeeze:
        counts_shape = node.count.shape
      elif isinstance(splits, int):
        counts_shape = (splits, *node.count.shape)
      else:
        counts_shape = (*splits, *node.count.shape)

      node.key = RngKey(key, tag=node.tag)
      node.count = RngCount(
        jnp.zeros(counts_shape, dtype=jnp.uint32), tag=node.tag
      )
    return node

  return graphlib.recursive_map(_split_stream, node, graph=graph)

