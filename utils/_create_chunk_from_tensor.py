
def _create_chunk_from_tensor(tensor: torch.Tensor) -> ChunkStorageMetadata:
    return ChunkStorageMetadata(
        offsets=torch.Size([0] * len(tensor.size())), sizes=tensor.size()
    )

