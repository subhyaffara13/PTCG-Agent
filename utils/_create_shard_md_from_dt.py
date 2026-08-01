
def _create_shard_md_from_dt(dt: DTensor, current_rank: int) -> ShardMetadata:
    mesh = dt.device_mesh
    if mesh.ndim != 1:
        raise AssertionError("Only 1D DeviceMeshes currently handled")

    offsets, sizes = _get_local_box(dt)
    return ShardMetadata(
        shard_offsets=list(offsets),
        shard_sizes=list(sizes),
        placement=f"rank:{current_rank}/{dt._local_tensor.device}",
    )

