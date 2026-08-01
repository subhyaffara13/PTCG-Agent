
def _all_gather_into_tensor_coalesced(input, tag, ranks, group_size):
    group_name = c10d._resolve_group_name_by_ranks_and_tag(ranks, tag)
    return torch.ops._c10d_functional.all_gather_into_tensor_coalesced(
        input,
        group_size,
        group_name,
    )

