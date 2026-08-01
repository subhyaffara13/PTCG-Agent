
def index_to_chunk_id(
    idx: Index, global_shape: Shape, shard_shape: Shape
) -> ChunkId:
  """Converts index to chunk id."""
  assert len(idx) == len(global_shape) == len(shard_shape)
  chunks = tuple([gs / ss for gs, ss in zip(global_shape, shard_shape)])
  chunk_id = [-1] * len(chunks)
  for d, sl in enumerate(idx):
    start = sl.start
    stop = sl.stop
    if start is None:
      start = 0
    if stop is None:
      stop = global_shape[d]
    assert sl.step == 1 or sl.step is None
    assert start % shard_shape[d] == 0 and stop % shard_shape[d] == 0
    assert stop - start == shard_shape[d]
    chunk_id[d] = start // shard_shape[d]
  return tuple(chunk_id)

