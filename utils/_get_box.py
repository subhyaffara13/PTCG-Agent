
def _get_box(tensor: DTensor) -> tuple[torch.Size, torch.Size]:
    device_mesh = tensor.device_mesh
    if device_mesh.ndim != 1:
        raise AssertionError("Only 1D DeviceMeshes currently handled")

    placement = tensor.placements[0]
    offsets = [0] * len(tensor.size())
    num_chunks = device_mesh.size(mesh_dim=0)

    # NOTE: is_shard() does not match _StridedShard; see _is_shard_like().
    if tensor.placements[0].is_shard():
        shard_dim = cast(DShard, placement).dim
        chunk_size = tensor.size(shard_dim) // num_chunks
        offsets[shard_dim] = chunk_size

    return (torch.Size(offsets), tensor._local_tensor.size())

