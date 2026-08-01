
def _create_chunk_dtensor(
    tensor: torch.Tensor,
    rank: int,
    device_mesh: DeviceMesh,
) -> DTensor:
    """
    Shard a tensor to chunks along the first dimension. The local rank will gets its
    corresponding chunk as the local tensor to create a DTensor.
    """
    # We need to explicitly call .detach() to return a new tensor detached from the current graph.
    tensor = tensor.detach().clone()

    # FSDP placements: [Shard(0)]
    # HSDP placements: [Replicate(), Shard(0)]
    replicate_placements = [Replicate() for _ in range(device_mesh.ndim)]
    shard_placements = [Replicate() for _ in range(device_mesh.ndim)]
    shard_placements[-1] = DShard(0)  # type: ignore[call-overload]

    return DTensor.from_local(
        tensor, device_mesh, replicate_placements, run_check=False
    ).redistribute(
        placements=shard_placements,
    )

