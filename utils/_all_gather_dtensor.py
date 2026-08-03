import copy

def _all_gather_dtensor(
    tensor: DTensor,
    root_mesh: DeviceMesh | None,
) -> torch.Tensor:
    """
    All gather a DTensor in its sharded dimension and return the local tensor.
    """
    if root_mesh != tensor.device_mesh:
        raise AssertionError("The device mesh of a tensor should be a root mesh.")

    placements = list(copy.deepcopy(tensor.placements))
    # FSDP placements: [Shard(0)] -> [Replicate()]
    # HSDP placements: [Replicate(), Shard(0)] -> [Replicate(), Replicate()]
    placements[-1] = Replicate()
    tensor = tensor.redistribute(
        device_mesh=tensor.device_mesh,
        placements=placements,
    )

    return tensor.to_local()


def _all_gather_dtensor(
    tensor: DTensor,
    parent_mesh: DeviceMesh | None,
) -> torch.Tensor:
    """All gather a DTensor in its FSDP dimension and return the local tensor."""
    if parent_mesh != tensor.device_mesh:
        raise AssertionError

    placements = list(copy.deepcopy(tensor.placements))
    # FSDP + TP: [Shard(0), tp_placement] -> [Replicate(), tp_placement]
    # HSDP + TP: [Replicate(), Shard(0), tp_placement] -> [Replicate(), Replicate(), tp_placement]
    for i in range(len(placements) - 1):
        placements[i] = Replicate()
    tensor = tensor.redistribute(
        device_mesh=tensor.device_mesh,
        placements=placements,
    )

    return tensor.to_local()

