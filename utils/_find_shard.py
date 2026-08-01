
def _find_shard(tensor: ShardedTensor, index: MetadataIndex) -> Shard:
    if index.offset is None:
        raise ValueError(
            f"Cannot lookup {index.fqn} since its a ShardedTensor and no offset was provided"
        )

    shards = tensor.local_shards()
    # index fast path
    if index.index is not None:
        if (
            len(shards) > index.index
            and torch.Size(shards[index.index].metadata.shard_offsets) == index.offset
        ):
            return shards[index.index]

    for shard in shards:
        if torch.Size(shard.metadata.shard_offsets) == index.offset:
            return shard
    raise ValueError(f"Could not find shard at '{index.offset}' for FQN: '{index.fqn}'")

