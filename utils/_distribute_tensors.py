
def _distribute_tensors(
    local_state_dict: dict[str, Any],
    keys: list[str],
    device: torch.device,
    pg: dist.ProcessGroup | None = None,
) -> None:
    if pg is None:
        pg = dist.distributed_c10d._get_default_group()
    for key in keys:
        _local_state = local_state_dict.get(key)
        if _local_state is None or torch.is_tensor(_local_state):
            continue

        local_state = _local_state[0]
        full_tensor = _local_state[1]

        shape, offset = compute_local_shape_and_global_offset(
            full_tensor.shape, local_state.device_mesh, local_state.placements
        )
        slices = [
            slice(cur_offset, cur_offset + cur_shape)
            for cur_shape, cur_offset in zip(shape, offset)
        ]
        if local_state.is_meta:
            # Use .clone() here rather than view to clone and return only the sliced portion, minimizing memory access and cost.
            local_tensor = full_tensor[tuple(slices)].detach().clone()
            # TODO: currently, we cannot handle strided sharding if the dp dimension is not even. For example,
            # one of the case that is not yet supported is when placements = (Shard(0), _StridedShard(0, sf=2)).
            ret = DTensor.from_local(
                local_tensor,
                local_state.device_mesh,
                local_state.placements,
                shape=local_state.shape,
                stride=local_state.stride(),
            )
        else:
            ret = local_state
            # Copy full_tensor[slices] into local_state.to_local() to reduce memory footprint.
            ret.to_local().copy_(full_tensor[tuple(slices)])
        local_state_dict[key] = ret

