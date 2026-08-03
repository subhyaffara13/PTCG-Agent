from typing import Any, Callable

def hook_with_zero_step(
    hook: Callable[[Any, dist.GradBucket], torch.futures.Future],
    ddp: DistributedDataParallel,
    zero: ZeroRedundancyOptimizer,
    shard_buckets: bool = False,
) -> Callable[[Any, dist.GradBucket], torch.futures.Future[torch.Tensor]]:
    r"""
    Modify ``hook`` to overlap :class:`ZeroRedundancyOptimizer` optimizer step with :class:`DistributedDataParallel` backward pass.

    This approach overlaps the optimizer computation and communication with the
    backward communication. In particular, the backward computation proceeds
    contiguously, and the optimizer computation follows, overlapping with
    outstanding backward communication (i.e. all-reduces) and possibly other
    optimizer communication (i.e. broadcasts).
    The optimizer step computation begins after the last gradient bucket computation has finished.

    This approach may be preferred over :meth:`hook_with_zero_step_interleaved`
    if communication is relatively slow compared to computation.

    Arguments:
        hook (Callable[[Any, dist.GradBucket], torch.futures.Future]): the hook
            to modify.
        ddp (DistributedDataParallel): the :class:`DistributedDataParallel`
            instance to use.
        zero (ZeroRedundancyOptimizer): the :class:`ZeroRedundancyOptimizer`
            instance to use.
        shard_buckets (bool): if ``True``, then the assignment of each
            :class:`DistributedDataParallel` bucket is partitioned across
            possibly multiple :class:`ZeroRedundancyOptimizer` instances (i.e.
            across possibly multiple ranks) to approximate uniformity; if
            ``False``, then each bucket is wholly assigned to a single
            :class:`ZeroRedundancyOptimizer` instance (i.e. to a single rank).

    Returns:
        The modified hook.

    Raises:
        ValueError: if ``zero`` was constructed with ``overlap_with_ddp=False``.
        RuntimeError: if using any backend other than NCCL/HCCL since currently
            Gloo may hang.

    .. warning::
        Given the way that overlapping :class:`DistributedDataParallel` with
        :class:`ZeroRedundancyOptimizer` is currently implemented, the first
        two or three training iterations do not perform parameter updates in
        the optimizer step, depending on if ``static_graph=False`` or
        ``static_graph=True``, respectively. This is because it needs
        information about the gradient bucketing strategy used by
        :class:`DistributedDataParallel`, which is not finalized until the
        second forward pass if ``static_graph=False`` or until the third
        forward pass if ``static_graph=True``.
    """
    if not zero._overlap_with_ddp:
        raise ValueError(
            "ZeroRedundancyOptimizer must be constructed with "
            "`overlap_with_ddp=True` to use this hook properly"
        )
    ddp_ref = weakref.ref(ddp)

    # NOTE: Gloo may hang with this overlapping approach; see https://github.com/pytorch/pytorch/issues/62300
    pg = dist.get_backend(ddp_ref().process_group)  # type: ignore[union-attr]
    if pg == dist.Backend.GLOO:
        raise RuntimeError(
            "Gloo backend using Overlapping DDP with ZeRO may meet hangs"
        )

    if shard_buckets:
        zero._overlap_info.shard_buckets = True
        zero._overlap_info.total_size = 0

    def hook_with_zero_fn(
        state: Any,
        bucket: dist.GradBucket,
    ) -> torch.futures.Future[torch.Tensor]:
        r"""
        Return :class:`Future` that runs the optimizer step if this corresponds to the last gradient bucket.

        Perform equivalent of :class:`ZeroRedundancyOptimizer` :meth:`step` if ``bucket`` is last gradient bucket.
        The function gives a gradient bucket tensor and
        performs additional computation on the iteration that
        the :class:`DistributedDataParallel` buckets are rebuilt to collect
        information used to implement the modified hook.

        Arguments:
            state (Any): any state for the hook.
            bucket (dist.GradBucket): the :class:`DistributedDataParallel`
                gradient bucket.
        """
        fut = hook(state, bucket)
        _hook_with_zero_step_setup(ddp_ref, zero, bucket)
        if zero._overlap_info.status != _OverlapStatus.INITIALIZED:
            return fut

        overlap_info = zero._overlap_info
        bucket_index = bucket.index()
        rank = zero.global_rank

        if overlap_info.status != _OverlapStatus.INITIALIZED:
            raise AssertionError
        if len(overlap_info.assigned_ranks_per_bucket) <= bucket_index:
            raise AssertionError("`assigned_ranks_per_bucket` is not fully constructed")
        assigned_to_bucket = (
            rank in overlap_info.assigned_ranks_per_bucket[bucket_index]
        )

        # Save the bucket reference and all-reduce future for the final bucket
        if assigned_to_bucket:
            overlap_info.bucket_index_to_bucket[bucket_index] = bucket
            overlap_info.bucket_index_to_future[bucket_index] = fut

        # Check that buckets are indexed incrementally starting from 0 in the
        # order of their autograd hooks firing
        if len(overlap_info.bucket_indices_seen) > 0:
            if overlap_info.bucket_indices_seen[-1] != bucket_index - 1:
                raise AssertionError("Bucket indices are not in incremental order")
        else:
            if bucket_index != 0:
                raise AssertionError("Bucket indices do not start from 0")
        overlap_info.bucket_indices_seen.append(bucket_index)

        # Directly return the future without any optimizer computation if this
        # is not the last bucket
        num_buckets = len(overlap_info.params_per_bucket)
        is_last_bucket = bucket_index == num_buckets - 1
        if not is_last_bucket:
            return fut

        # Perform partial optimizer step on all buckets after the final
        # bucket has been computed
        # NOTE: This should not be chained as a callback to the last bucket's
        # all-reduce future since that would add synchronization that delays
        # all optimizer computation to wait for that last all-reduce
        for bucket_index in range(num_buckets):
            assigned_ranks = overlap_info.assigned_ranks_per_bucket[bucket_index]
            if rank in assigned_ranks:
                # Wait on the bucket's all-reduce future to ensure correct
                # gradients
                if bucket_index not in overlap_info.bucket_index_to_future:
                    raise AssertionError(
                        f"All-reduce future for bucket {bucket_index} not saved "
                        f"on rank {rank}"
                    )
                allreduce_future = overlap_info.bucket_index_to_future[bucket_index]
                allreduce_future.wait()

                # Perform the partial optimizer step
                curr_bucket = overlap_info.bucket_index_to_bucket[bucket_index]
                _perform_local_step(curr_bucket, zero, rank)

            _broadcast_bucket(bucket_index, zero)

        # Ensure that all parameter updates are finished before the
        # next forward pass
        overlap_info.wait_for_broadcasts()
        overlap_info.clear_per_iter_info()

        return fut

    return hook_with_zero_fn

