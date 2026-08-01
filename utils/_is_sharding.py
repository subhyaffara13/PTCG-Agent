
def _is_sharding(p: Placement) -> TypeIs[Shard | _StridedShard]:
    return isinstance(p, (Shard, _StridedShard))

