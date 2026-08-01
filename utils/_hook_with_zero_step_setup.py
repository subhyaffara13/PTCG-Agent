
def _hook_with_zero_step_setup(
    ddp_ref: weakref.ReferenceType,
    zero: ZeroRedundancyOptimizer,
    bucket: dist.GradBucket,
):
    r"""
    Encapsulate the setup logic for :func:`hook_with_zero_step` and :func:`hook_with_zero_step_interleaved`.

    This means the logic to run in the
    hook before the backward pass and optimizer step can actually be
    overlapped. This is factored out since it is common to both
    :func:`hook_with_zero_step` and :func:`hook_with_zero_step_interleaved`.

    Arguments:
        ddp_ref (weakref.ReferenceType): weak reference to the process's
            :class:`DistributedDataParallel` instance.
        zero (ZeroRedundancyOptimizer): the calling process's
            :class:`ZeroRedundancyOptimizer` instance.
        bucket (dist.GradBucket): the current gradient bucket.
    """
    # Proceed as normal until the DDP buckets have been rebuilt
    if not ddp_ref()._has_rebuilt_buckets:  # type: ignore[union-attr]
        if zero._overlap_info.status != _OverlapStatus.UNINITIALIZED:
            raise AssertionError
        return

    bucket_index = bucket.index()
    overlap_info = zero._overlap_info
    if overlap_info.status == _OverlapStatus.UNINITIALIZED:
        overlap_info.status = _OverlapStatus.DDP_HAS_REBUILT_BUCKETS

    if overlap_info.status == _OverlapStatus.DDP_HAS_REBUILT_BUCKETS:
        if bucket_index == 0 and len(overlap_info.params_per_bucket) > 0:
            # This corresponds to the first bucket of the backward pass
            # immediately after all information has been saved, so we
            # can perform the delayed ZeRO initialization
            zero._init_zero_for_overlap()
        else:
            # Once DDP buckets have been rebuilt but ZeRO has not been
            # properly initialized yet, save the information needed
            _save_ddp_bucket_info(bucket, zero)

