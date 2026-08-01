
def all_reduce(inputs, outputs=None, op=SUM, streams=None, comms=None):
    _check_sequence_type(inputs)
    if outputs is None:
        outputs = inputs
    _check_sequence_type(outputs)
    torch._C._nccl_all_reduce(inputs, outputs, op, streams, comms)


def all_reduce(tensor, op=ReduceOp.SUM, group=None, async_op: bool = False):
    """
    Reduces the tensor data across all machines in a way that all get the final result.

    After the call ``tensor`` is going to be bitwise identical in all processes.

    Complex tensors are supported.

    Args:
        tensor (Tensor): Input and output of the collective. The function
            operates in-place.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    Examples:
        >>> # xdoctest: +SKIP("no rank")
        >>> # All tensors below are of torch.int64 type.
        >>> # We have 2 process groups, 2 ranks.
        >>> device = torch.device(f"cuda:{rank}")
        >>> tensor = torch.arange(2, dtype=torch.int64, device=device) + 1 + 2 * rank
        >>> tensor
        tensor([1, 2], device='cuda:0') # Rank 0
        tensor([3, 4], device='cuda:1') # Rank 1
        >>> dist.all_reduce(tensor, op=ReduceOp.SUM)
        >>> tensor
        tensor([4, 6], device='cuda:0') # Rank 0
        tensor([4, 6], device='cuda:1') # Rank 1

        >>> # All tensors below are of torch.cfloat type.
        >>> # We have 2 process groups, 2 ranks.
        >>> tensor = torch.tensor(
        ...     [1 + 1j, 2 + 2j], dtype=torch.cfloat, device=device
        ... ) + 2 * rank * (1 + 1j)
        >>> tensor
        tensor([1.+1.j, 2.+2.j], device='cuda:0') # Rank 0
        tensor([3.+3.j, 4.+4.j], device='cuda:1') # Rank 1
        >>> dist.all_reduce(tensor, op=ReduceOp.SUM)
        >>> tensor
        tensor([4.+4.j, 6.+6.j], device='cuda:0') # Rank 0
        tensor([4.+4.j, 6.+6.j], device='cuda:1') # Rank 1

    """
    # Dynamo has built-in logic to map legacy distributed ops to functional collectives.
    # Let's redirect to a torch function mode that can mimic this logic outside Dynamo
    # (e.g., non-strict export implements such a torch function mode).
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            all_reduce,
            relevant_args,
            tensor,
            op=op,
            group=group,
            async_op=async_op,
        )

    _check_single_tensor(tensor, "tensor")
    if _rank_not_in_group(group):
        _warn_not_in_group("all_reduce")
        return

    if tensor.is_complex():
        if not supports_complex(op):
            raise ValueError(f"all_reduce does not support {op} on complex tensors")
        tensor = torch.view_as_real(tensor)

    opts = AllreduceOptions()
    opts.reduceOp = op
    opts.asyncOp = async_op
    if group is None:
        group = _get_default_group()

    if group in _world.pg_coalesce_state:
        # We are in coalescing context, do not issue single operation, just append a collective representation
        coll = _CollOp(all_reduce, tensor, None, op, None)
        _world.pg_coalesce_state[group].append(coll)
        if async_op:
            return _IllegalWork()
        else:
            return None

    work = group.allreduce([tensor], opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def all_reduce(self: torch.Tensor, reduceOp: str, group: RANK_TYPES, tag: str = ""):
    """
    Reduces the tensor data across all machines in such a way that all get
    the final result.

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
    tensor = torch.ops._c10d_functional.all_reduce(
        self, reduceOp.lower(), _group_or_group_name(group)
    )
    return _maybe_wrap_tensor(tensor)


def all_reduce(tensor, op=ReduceOp.SUM, group=group.WORLD):
    """
    Reduces the tensor data across all machines in such a way that all get the final result.

    After the call the returned tensor is going to be bitwise
    identical in all processes.

    Arguments:
        tensor (Tensor): Input of the collective.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        Tensor: Output of the collective

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile(
            "all_reduce",
            suggestion="torch.distributed._functional_collectives.all_reduce",
        )
    _deprecated("all_reduce", "torch.distributed._functional_collectives.all_reduce")
    return _AllReduce.apply(op, group, tensor)


def all_reduce(output: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.VectorType], dim: _Union[int, _ods_ir.IntegerAttr], kind: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return AllReduceOp(output=output, input=input, dim=dim, kind=kind, loc=loc, ip=ip).result


def all_reduce(value: _ods_ir.Value, *, op: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, uniform: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AllReduceOp(value=value, op=op, uniform=uniform, results=results, loc=loc, ip=ip).result


def all_reduce(result: _Sequence[_ods_ir.Type], operands_: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, use_global_device_ids: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllReduceOp]:
  op = AllReduceOp(result=result, operands_=operands_, replica_groups=replica_groups, channel_handle=channel_handle, use_global_device_ids=use_global_device_ids, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def all_reduce(tensor: _ods_ir.Value, reduction_axes: _Union[_Any, _ods_ir.Attribute], out_sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AllReduceOp(tensor=tensor, reduction_axes=reduction_axes, out_sharding=out_sharding, results=results, loc=loc, ip=ip).result


def all_reduce(result: _Sequence[_ods_ir.Type], operands_: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, use_global_device_ids: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllReduceOp]:
  op = AllReduceOp(result=result, operands_=operands_, replica_groups=replica_groups, channel_handle=channel_handle, use_global_device_ids=use_global_device_ids, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)

