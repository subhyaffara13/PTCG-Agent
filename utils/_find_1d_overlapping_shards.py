
def _find_1d_overlapping_shards(
    shards: list[ShardMetadata], dim: int
) -> tuple[int, int] | None:
    # (begin, end, index_in_shards). Begin and end are inclusive.
    intervals = [
        (s.shard_offsets[dim], s.shard_offsets[dim] + s.shard_sizes[dim] - 1, i)
        for i, s in enumerate(shards)
    ]
    intervals.sort()
    for i in range(len(shards) - 1):
        if intervals[i][1] >= intervals[i + 1][0]:
            return (intervals[i][2], intervals[i + 1][2])
    return None

