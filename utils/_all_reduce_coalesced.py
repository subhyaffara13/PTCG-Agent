
def _all_reduce_coalesced(inputs, reduce_op, tag, ranks, group_size):
    group_name = c10d._resolve_group_name_by_ranks_and_tag(ranks, tag)
    return torch.ops._c10d_functional.all_reduce_coalesced(
        inputs,
        reduce_op,
        group_name,
    )

