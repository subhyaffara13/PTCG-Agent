
def _shard_mutable_array(xs, shardings, layouts, copy_semantics):
  bufs = [x._refs._buf for x in xs]
  return shard_args(shardings, layouts, copy_semantics, bufs)

