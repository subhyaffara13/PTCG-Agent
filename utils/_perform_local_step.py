
def _perform_local_step(
    bucket: dist.GradBucket,
    zero: ZeroRedundancyOptimizer,
    rank: int,
):
    r"""
    Perform a local optimizer step using the gradients provided by ``bucket``.

    Arguments:
        bucket (dist.GradBucket): the bucket providing the gradients.
        zero (ZeroRedundancyOptimizer): the :class:`ZeroRedundancyOptimizer`
            instance to perform the :meth:`_local_step`.
        rank (int): the calling process's rank.

    .. warning::
        This function assumes that appropriate synchronization has taken place
        so that the bucket's gradients can be used.
    """
    overlap_info = zero._overlap_info
    bucket_index = bucket.index()
    if len(zero.optim.param_groups) != 1:
        raise AssertionError(
            "Overlapping DDP with ZeRO only supports a single parameter group"
        )

    # Construct the `gradients` input for the local optimizer step, which
    # expects `None` in a list position to indicate that the corresponding
    # parameter should not be updated
    num_local_optim_params = len(zero.optim.param_groups[0]["params"])
    gradients: list[torch.Tensor | None] = [
        _NO_PARAM_UPDATE for _ in range(num_local_optim_params)
    ]
    if bucket_index not in overlap_info.offsets:
        raise AssertionError(
            f"Bucket index {bucket_index} was not assigned to rank {rank}"
        )
    gradients_offset = overlap_info.offsets[bucket_index]
    bucket_assignment = zero._bucket_assignments_per_rank[rank][bucket_index]
    bucket_offset = bucket_assignment.offset
    length = len(bucket_assignment.parameters)
    bucket_gradients = bucket.gradients()[bucket_offset : bucket_offset + length]
    for i, grad in enumerate(bucket_gradients):
        gradients[gradients_offset + i] = grad

    zero._local_step(gradients)

