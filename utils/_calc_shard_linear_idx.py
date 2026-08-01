
def _calc_shard_linear_idx(
    shard_coord: Sequence[IntLikeType], shard_size: Sequence[IntLikeType]
) -> IntLikeType:
    # compute shard linear index
    shard_linear_idx: IntLikeType = 0
    shard_coord_stride: IntLikeType = 1
    for idx, size in zip(reversed(shard_coord), reversed(shard_size)):
        shard_linear_idx += idx * shard_coord_stride
        shard_coord_stride *= size

    return shard_linear_idx

