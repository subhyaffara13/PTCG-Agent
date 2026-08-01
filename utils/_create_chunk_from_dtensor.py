
def _create_chunk_from_dtensor(tensor: DTensor) -> ChunkStorageMetadata:
    sizes, offsets = compute_local_shape_and_global_offset(
        tensor.shape, tensor.device_mesh, tensor.placements
    )
    sizes, offsets = torch.Size(sizes), torch.Size(offsets)
    return ChunkStorageMetadata(
        offsets=offsets,
        sizes=sizes,
    )

