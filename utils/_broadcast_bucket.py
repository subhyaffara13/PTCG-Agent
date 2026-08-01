
def _broadcast_bucket(
    bucket_index: int,
    zero: ZeroRedundancyOptimizer,
):
    r"""
    Broadcasts a bucket's parameters.

    Arguments:
        bucket_index (int): the index of the bucket corresponding to the
            parameters to broadcast.
        zero (ZeroRedundancyOptimizer): the calling process's
            :class:`ZeroRedundancyOptimizer` instance.
    """
    overlap_info = zero._overlap_info
    if len(overlap_info.assigned_ranks_per_bucket) <= bucket_index:
        raise AssertionError("`assigned_ranks_per_bucket` is not fully constructed")
    # Sort to ensure the same ordering across ranks
    assigned_ranks = sorted(overlap_info.assigned_ranks_per_bucket[bucket_index])
    if len(assigned_ranks) <= 0:
        raise AssertionError(
            f"Bucket {bucket_index} should be assigned to at least one rank"
        )
    for assigned_rank in assigned_ranks:
        bucket_assignments = zero._bucket_assignments_per_rank[assigned_rank]
        if bucket_index in bucket_assignments:
            send_tensor = bucket_assignments[bucket_index].tensor
            if send_tensor is None:
                raise AssertionError
            overlap_info.broadcast_handles.append(
                dist.broadcast(
                    send_tensor,
                    src=dist.get_global_rank(zero.process_group, assigned_rank),
                    group=zero.process_group,
                    async_op=True,
                )
            )

