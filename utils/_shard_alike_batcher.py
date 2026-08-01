
def _shard_alike_batcher(batched_args, batch_dims):
  x, y = batched_args
  xd, yd = batch_dims
  if xd == yd:
    return shard_alike(x, y), (xd, yd)
  elif xd is None:
    x = batching.broadcast(x, y.shape[yd], yd, None)
    return shard_alike(x, y), (yd, yd)
  elif yd is None:
    y = batching.broadcast(y, x.shape[xd], xd, None)
    return shard_alike(x, y), (xd, xd)
  else:
    y = batching.moveaxis(y, yd, xd)
    return shard_alike(x, y), (xd, xd)

