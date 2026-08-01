
def reduce_scatter_tensor(output, input, op=ReduceOp.SUM, group=None, async_op=False):
    """
    Reduces, then scatters a tensor to all ranks in a group.

    Args:
        output (Tensor): Output tensor. It should have the same size across all
            ranks.
        input (Tensor): Input tensor to be reduced and scattered. Its size
            should be output tensor size times the world size. The input tensor
            can have one of the following shapes:
            (i) a concatenation of the output tensors along the primary
            dimension, or
            (ii) a stack of the output tensors along the primary dimension.
            For definition of "concatenation", see ``torch.cat()``.
            For definition of "stack", see ``torch.stack()``.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group.

    Examples:
        >>> # xdoctest: +SKIP("need process group init")
        >>> # All tensors below are of torch.int64 dtype and on CUDA devices.
        >>> # We have two ranks.
        >>> device = torch.device(f"cuda:{rank}")
        >>> tensor_out = torch.zeros(2, dtype=torch.int64, device=device)
        >>> # Input in concatenation form
        >>> tensor_in = torch.arange(world_size * 2, dtype=torch.int64, device=device)
        >>> tensor_in
        tensor([0, 1, 2, 3], device='cuda:0') # Rank 0
        tensor([0, 1, 2, 3], device='cuda:1') # Rank 1
        >>> dist.reduce_scatter_tensor(tensor_out, tensor_in)
        >>> tensor_out
        tensor([0, 2], device='cuda:0') # Rank 0
        tensor([4, 6], device='cuda:1') # Rank 1
        >>> # Input in stack form
        >>> tensor_in = torch.reshape(tensor_in, (world_size, 2))
        >>> tensor_in
        tensor([[0, 1],
                [2, 3]], device='cuda:0') # Rank 0
        tensor([[0, 1],
                [2, 3]], device='cuda:1') # Rank 1
        >>> dist.reduce_scatter_tensor(tensor_out, tensor_in)
        >>> tensor_out
        tensor([0, 2], device='cuda:0') # Rank 0
        tensor([4, 6], device='cuda:1') # Rank 1

    """
    # Dynamo has built-in logic to map legacy distributed ops to functional collectives.
    # Let's redirect to a torch function mode that can mimic this logic outside Dynamo
    # (e.g., non-strict export implements such a torch function mode).
    relevant_args = (input,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            reduce_scatter_tensor,
            relevant_args,
            output,
            input,
            op=op,
            group=group,
            async_op=async_op,
        )

    _check_single_tensor(output, "output")
    _check_single_tensor(input, "input")

    if _rank_not_in_group(group):
        _warn_not_in_group("reduce_scatter_tensor")
        return

    opts = ReduceScatterOptions()
    opts.reduceOp = op
    opts.asyncOp = async_op

    group = group or _get_default_group()

    # Check if we are in coalescing context
    # If we are, do not issue single operation, just append a collective representation
    if group in _world.pg_coalesce_state:
        coll = _CollOp(reduce_scatter_tensor, input, output, op, None)
        _world.pg_coalesce_state[group].append(coll)
        if async_op:
            return _IllegalWork()
        else:
            return None

    work = group._reduce_scatter_base(output, input, opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def reduce_scatter_tensor(
    self: torch.Tensor,
    reduceOp: str,
    scatter_dim: int,
    group: RANK_TYPES,
    tag: str = "",
):
    """
    Reduces the tensor data across all machines in such a way that all get
    the final result, then scatter the results to corresponding ranks.


    The input tensor is left unmodified.
    Group can be one of:
        List[int]: ranks participating in the collective.
        List[List[int]]: 2D mesh of ranks taking part of this collective in MPMD.
        ProcessGroup: Will perform a collective using the ranks and tag of the PG.
        DeviceMesh: Do a SPMD collective over all ranks of the mesh
        (DeviceMesh, int): Do a MPMD collective over one dimension of the DeviceMesh
    :: N.B. If you pass a PG or a 1D list to perform a MPMD collective, the compiler won't be able to recover
    that information and perform collective algebraic optimization. Use other forms of input for that.
    """
    group = _resolve_group(group, tag)
    group_size = c10d._get_group_size_by_name(group)

    if self.size(scatter_dim) % group_size != 0:
        raise AssertionError(
            f"input dimension 0 ({self.size(0)} must be a multiple of group_size {group_size})"
        )
    if scatter_dim != 0:
        self = _chunk_or_narrow_cat(self, group_size, narrow_dim=scatter_dim, cat_dim=0)

    tensor = torch.ops._c10d_functional.reduce_scatter_tensor(
        self,
        reduceOp.lower(),
        group_size,
        _group_or_group_name(group),
    )
    res = _maybe_wrap_tensor(tensor)
    return res

