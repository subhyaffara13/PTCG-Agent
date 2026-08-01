
def _shard_tensors(
    tensors: list[tuple[str, torch.Tensor]],
    input_placements: tuple[Placement, ...],
    world_size: int,
    mesh: DeviceMesh,
    mask_shift: int = 0,
) -> list[LocalTensor | torch.Tensor]:
    """Create sharded LocalTensors from tensors according to placements."""
    local_tensors: list[LocalTensor | torch.Tensor] = []
    for tensor_idx, ((name, tensor), placement) in enumerate(
        zip(tensors, input_placements)
    ):
        if isinstance(placement, Partial):
            local_tensor = _create_partial_input(
                tensor, placement, world_size, tensor_idx, mask_shift
            )
        elif isinstance(placement, Replicate):
            _tmp = {r: tensor.clone() for r in range(world_size)}
            # pyrefly: ignore [bad-argument-type, bad-argument-count]
            local_tensor = LocalTensor(_tmp)
        elif isinstance(placement, Shard):
            shard_dim = placement.dim
            chunks = tensor.tensor_split(world_size, dim=shard_dim)
            _tmp = {
                r: chunks[r].clone(memory_format=torch.contiguous_format)
                for r in range(world_size)
            }
            # pyrefly: ignore [bad-argument-type, bad-argument-count]
            local_tensor = LocalTensor(_tmp)
        else:
            dt = distribute_tensor(tensor.clone(), mesh, (placement,))
            local_tensor = dt.to_local()
        local_tensors.append(local_tensor)
    return local_tensors

