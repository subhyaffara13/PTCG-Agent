
def bucket_all_gather_by_mb(
    gm: torch.fx.GraphModule,
    bucket_cap_mb_by_bucket_idx: Callable[[int], float],
    filter_wait_node: Callable[[torch.fx.Node], bool] | None = None,
    mode: BucketMode | None = None,
) -> list[list[torch.fx.Node]]:
    """
    Identifies all all_gather nodes and groups them into buckets,
    based on size limit `bucket_cap_mb_by_bucket_idx`.

    Args:
        gm (torch.fx.GraphModule): GraphModule where to bucket all_gathers.
        bucket_cap_mb_by_bucket_idx (Callable[[int], float]): Callable to specify cap of the bucket
            in megabytes by bucket idx.  The idea of `bucket_cap_mb_by_bucket_idx` is to allow
            to specify different sizes of the buckets at the start,
            as first all_gather is usually exposed.  Interface of bucket_cap_mb_by_bucket_idx
            is `bucket_cap_mb_by_bucket_idx_default` function that is default value for `bucket_cap_mb_by_bucket_idx`.
        filter_wait_node (Callable[[torch.fx.Node], bool] | None): If specified,
            only all_gather nodes with wait_node that satisfy `filter_wait_node` will be bucketed.

    Returns:
        list[list[torch.fx.Node]]: List of buckets, where each bucket is a list of all_gather nodes.
    """
    mode = mode or _default_bucket_mode()

    group_key_fn = (
        _ag_group_key_multidtype if mode and "multidtype" in mode else _ag_group_key
    )

    return greedy_bucket_collective_by_mb(
        gm,
        bucket_cap_mb_by_bucket_idx,
        is_all_gather_into_tensor,
        group_key_fn,
        filter_wait_node,
    )

