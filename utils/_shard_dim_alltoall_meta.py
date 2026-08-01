
def _shard_dim_alltoall_meta(
    input, gather_dim, shard_dim, group_name: GroupName | ProcessGroup
):
    if isinstance(group_name, str):
        # pyrefly: ignore[bad-argument-type]  # pyrefly bug
        group_name = _resolve_process_group(group_name)
    group_size = group_name.size()
    stacked_list = [torch.empty_like(input) for _ in range(group_size)]
    group_rank = get_group_rank(group_name, get_rank())

    cat_tensor = torch.cat(stacked_list, dim=gather_dim)
    # pyrefly: ignore [unsupported-operation]
    chunk_size = cat_tensor.size(shard_dim) // group_size
    chunk = torch.narrow(cat_tensor, shard_dim, group_rank * chunk_size, chunk_size)
    return chunk.contiguous()

