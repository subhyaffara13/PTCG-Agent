
def reduce_scatter_offset(
    input: torch.Tensor,
    out: list[torch.Tensor],
    group: str,
    *,
    dim: int,
    offsets: list[int] | None = None,
    dst_ranks: list[int] | None = None,
    red_op: str = "sum",
) -> None:
    r"""
    reduce_scatter_offset(input, out, group, *, dim, offsets, dst_ranks, red_op='sum') -> None

    Simultaneously reduce N blocks of a 2-D ``input`` tensor from a symmetric
    memory buffer, routing each block to a specific destination rank.  Only
    ``dst_ranks[i]`` writes the reduced result for block ``i``; the result is
    written to a contiguous output tensor, with the same shape as block ``i``.

    The ``dim`` argument controls which dimension is sharded:

    - ``dim=0`` (row sharding): block ``i`` spans
      ``input[offsets[i-1] : offsets[i], :]``.  Each ``out[j]`` has shape
      ``(size_j, input.size(1))``.
    - ``dim=1`` (column sharding): block ``i`` spans
      ``input[:, offsets[i-1] : offsets[i]]``.  Each ``out[j]`` has shape
      ``(input.size(0), size_j)``.

    Blocks are described by ``offsets``, an inclusive prefix-sum of block sizes
    along ``dim`` (first block starts at index 0 by convention).  Block offsets
    can be even or uneven; when uneven, the following condition must be met: for
    each ``j``, the ``j``-th owned block must have the same size across all
    ranks (so that ``out[j]`` has a uniform shape); different ``j``'s may
    differ.

    Args:
        input (Tensor): 2-D tensor allocated via symmetric memory (innermost
            dimension must be contiguous).
        out (list[Tensor]): Output tensors for this rank's owned blocks.  Must
            have length equal to the number of blocks owned by this rank (i.e.
            the count of ``i`` where ``dst_ranks[i] == my_rank``).  Each
            ``out[j]`` must be contiguous with the same dtype as ``input``.
        group (str): The name of the ``ProcessGroup`` to perform the operation on.
        dim (int): Dimension along which blocks are defined (0 or 1).
        offsets (list[int] | None): Inclusive prefix-sum of block sizes along
            ``dim``, length N.  If not provided, ``input.size(dim)`` is divided
            into equal-size blocks based on the size of the ``group``.
        dst_ranks (list[int] | None): Destination rank for each block.  If not
            provided, blocks are distributed round-robin across ranks.
        red_op (str): Reduction operation; currently only ``'sum'`` is supported.

    Example::

        >>> # doctest: +SKIP
        >>> # Each rank holds a Grouped GEMM gradient buffer in symmetric memory.
        >>> # The buffer has W experts laid out as equal column blocks; each expert
        >>> # is reduced to a specific rank (dst_ranks[i] == i % world_size).
        >>> buf = symm_mem.empty(H, W * C, dtype=torch.bfloat16, device="cuda")
        >>> symm_mem.rendezvous(buf, group=group_name)
        >>> offsets = [i * C for i in range(1, W + 1)]  # inclusive prefix-sum
        >>> dst_ranks = [i % world_size for i in range(W)]
        >>> n_owned = sum(r == rank for r in dst_ranks)
        >>> out = [torch.empty(H, C, dtype=torch.bfloat16, device="cuda") for _ in range(n_owned)]
        >>> symm_mem.reduce_scatter_offset(buf, out, group_name, dim=1, offsets=offsets, dst_ranks=dst_ranks)
    """
    backend = get_backend(input.device)
    if backend == "NCCL":
        torch.ops.symm_mem.nccl_reduce_scatter_offset(
            input, out, group, dim, offsets, dst_ranks, red_op
        )
    else:
        raise NotImplementedError(
            f"reduce_scatter_offset: unsupported backend: {backend}"
        )

