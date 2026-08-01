
def _should_use_multimem_all_gather_matmul(
    A_shard: torch.Tensor,
    gather_dim: int,
    group_name: c10d.GroupName,
    return_A: bool,
) -> bool:
    group = c10d._resolve_process_group(group_name)
    local_M = math.prod(A_shard.shape[:-1])
    has_multicast_support = (
        A_shard.device.type == "cuda"
        and _SymmetricMemory.has_multicast_support(
            DeviceType.CUDA, A_shard.device.index
        )
    )

    return (
        has_multicast_support
        and not return_A
        and A_shard.is_contiguous()
        and gather_dim == 0
        # The heuristic is empirical. We could refine it with a more
        # sophisticated perf model.
        and local_M * group.size() <= 2048
    )

