
def chunk_id_to_index(chunk_id: ChunkId, shard_shape: Shape) -> Index:
  """Converts chunk id to index."""
  assert len(chunk_id) == len(shard_shape)
  idx = []
  for d, dim_id in enumerate(chunk_id):
    start = dim_id * shard_shape[d]
    stop = start + shard_shape[d]
    idx.append(slice(start, stop))
  assert len(idx) == len(shard_shape)
  return tuple(idx)

