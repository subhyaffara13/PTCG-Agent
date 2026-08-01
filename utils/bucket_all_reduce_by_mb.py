
def bucket_all_reduce_by_mb(
    gm: torch.fx.GraphModule,
    bucket_cap_mb_by_bucket_idx: Callable[[int], float],
    filter_wait_node: Callable[[torch.fx.Node], bool] | None = None,
) -> list[list[torch.fx.Node]]:
    return greedy_bucket_collective_by_mb(
        gm,
        bucket_cap_mb_by_bucket_idx,
        is_all_reduce_tensor,
        _ar_group_key,
        filter_wait_node,
    )

