
def shard_alike_lowering(ctx, x, y):
  return _group_shard(ctx, x, y, *ctx.avals_out)

