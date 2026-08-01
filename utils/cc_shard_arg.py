
def cc_shard_arg(x, sharding, layout):
  return shard_args([sharding], [layout], [xc.ArrayCopySemantics.REUSE_INPUT],
                    [x])[0]

