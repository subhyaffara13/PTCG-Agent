
def _save_ddp_bucket_info(
    bucket: dist.GradBucket,
    zero: ZeroRedundancyOptimizer,
):
    r"""
    Save :class:`DistributedDataParallel` gradient bucket information for :class:`ZeroRedundancyOptimizer` instance ``zero``.

    In particular, this function is meant to be called upon seeing each
    gradient bucket to use when overlapping, meaning it does not save or compute any global
    information.

    Arguments:
        bucket (dist.GradBucket): the current gradient bucket.
        zero (ZeroRedundancyOptimizer): the calling process's
            :class:`ZeroRedundancyOptimizer` instance.
    """
    overlap_info = zero._overlap_info
    bucket_params = bucket.parameters()
    if len(bucket_params) <= 0:
        raise AssertionError("Empty bucket")

    # Save the parameters in the bucket
    overlap_info.params_per_bucket.append(bucket_params)
    if overlap_info.shard_buckets:
        # Additionally save the bucket size for the assignment heuristic to use
        bucket_size = 0
        for param in bucket_params:
            bucket_size += param.numel()
        if overlap_info.total_size is None:
            raise AssertionError
        overlap_info.total_size += bucket_size

