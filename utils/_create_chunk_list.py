
def _create_chunk_list(tensor: torch.Tensor) -> list[ChunkStorageMetadata]:
    if hasattr(tensor, "__create_chunk_list__"):
        # DTensor implements _Checkpointable
        local_chunks = tensor.__create_chunk_list__()  # type: ignore[attr-defined]
    elif isinstance(tensor, ShardedTensor):
        local_chunks = [
            _chunk_for_shard(shard.metadata) for shard in tensor.local_shards()
        ]
    elif isinstance(tensor, torch.Tensor):
        local_chunks = [_create_chunk_from_tensor(tensor)]
    else:
        raise ValueError(
            "Unsupported Type, expecting one of [Tensor, DTensor, ShardedTensor] "
            f",but got {type(tensor)}"
        )

    return local_chunks

