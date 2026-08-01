
def _check_box_overlap(box0: ChunkStorageMetadata, box1: ChunkStorageMetadata) -> bool:
    """Check if two boxes overlap. Tuples are (offset, lengths)."""
    # For each dim of each shard, check if one shard resides on the other
    # end of second shard with respect to that dim. As an example for a 2D
    # shard, we would check if one shard is above or on the left of the
    # other shard.
    ndims = len(box0.offsets)
    for i in range(ndims):
        if box0.offsets[i] >= box1.offsets[i] + box1.sizes[i]:
            return False
        if box1.offsets[i] >= box0.offsets[i] + box0.sizes[i]:
            return False

    return True

