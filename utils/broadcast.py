
def broadcast(
    inputs: Sequence[torch.Tensor], root: int = 0, streams=None, comms=None
) -> None:
    _check_sequence_type(inputs)
    torch._C._nccl_broadcast(inputs, root, streams, comms)


def broadcast(
    data_or_fn: T | Callable[[], T],
    *,
    success: bool = True,
    stage_name: str | None = None,
    rank: int = 0,
    pg: dist.ProcessGroup | None = None,
) -> T:
    """
    Broadcasts the data payload from rank 0 to all other ranks.
    Or if a function is passed, execute it in rank 0 and broadcast result to all other ranks.

    Can be used to broadcast a failure signal to stop all ranks.

    If the function raises an exception, all ranks will raise.

    Args:
        data_or_fn: the data to broadcast or function to execute and broadcast result.
        success: False to stop all ranks.
        stage_name: the name of the logical stage for synchronization and debugging
        rank: rank to broadcast data or execute function and broadcast results.
        pg: the process group for sync
    Throws:
        RuntimeError from original exception trace
    Returns:
        the value after synchronization

    Example usage:
    >> id = broadcast(data_or_fn=allocate_id, rank=0, pg=ext_pg.my_pg)
    """

    if not success and data_or_fn is not None:
        raise AssertionError(
            "Data or Function is expected to be None if not successful"
        )

    payload: T | None = None
    exception: Exception | None = None
    # if no pg is passed then execute if rank is 0
    if (pg is None and rank == 0) or (pg is not None and pg.rank() == rank):
        # determine if it is an executable function or data payload only
        if callable(data_or_fn):
            try:
                payload = data_or_fn()
            except Exception as e:
                success = False
                exception = e
        else:
            payload = data_or_fn

    # broadcast the exception type if any to all ranks for failure categorization
    sync_obj = SyncPayload(
        stage_name=stage_name,
        success=success,
        payload=payload,
        exception=exception,
    )

    if pg is not None:
        broadcast_list = [sync_obj]
        dist.broadcast_object_list(broadcast_list, src=rank, group=pg)
        if len(broadcast_list) != 1:
            raise AssertionError(
                f"Expected broadcast_list to have exactly 1 element, got {len(broadcast_list)}"
            )
        sync_obj = broadcast_list[0]

    # failure in any rank will trigger a throw in every rank.
    if not sync_obj.success:
        error_msg = f"Rank {rank} failed"
        if stage_name is not None:
            error_msg += f": stage {sync_obj.stage_name}"
        if sync_obj.exception is not None:
            error_msg += f": exception {sync_obj.exception}"

        raise RuntimeError(error_msg) from sync_obj.exception

    return cast(T, sync_obj.payload)


def broadcast(
    tensor: torch.Tensor,
    src: int | None = None,
    group: ProcessGroup | None = None,
    async_op: bool = False,
    group_src: int | None = None,
):
    """
    Broadcasts the tensor to the whole group.

    ``tensor`` must have the same number of elements in all processes
    participating in the collective.

    Args:
        tensor (Tensor): Data to be sent if ``src`` is the rank of current
            process, and tensor to be used to save received data otherwise.
        src (int): Source rank on global process group (regardless of ``group`` argument).
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        group_src (int): Source rank on ``group``.  Must specify one of ``group_src``
            and ``src`` but not both.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            broadcast,
            relevant_args,
            tensor,
            src=src,
            group=group,
            async_op=async_op,
            group_src=group_src,
        )

    group = _group_or_default_group(group)
    group_src = _canonicalize_group_rank(group, src, group_src, return_global=False)
    _check_single_tensor(tensor, "tensor")
    if _rank_not_in_group(group):
        _warn_not_in_group("broadcast")
        return

    opts = BroadcastOptions()
    opts.rootRank = group_src
    opts.rootTensor = 0
    opts.asyncOp = async_op
    sm90_or_more = not (
        tensor.is_cuda and torch.cuda.get_device_capability(tensor.device)[0] >= 9
    )
    if tensor.is_complex():
        tensor = torch.view_as_real(tensor)
    elif _is_fp8(tensor) and not sm90_or_more:
        # FP8 is supported by NCCL on sm90+, use workaround for older GPUs
        tensor = tensor.view(torch.uint8)
    work = group.broadcast([tensor], opts)
    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def broadcast(self: torch.Tensor, src: int, group: RANK_TYPES, tag: str = ""):
    """
    Broadcasts the tensor to all processes in the given process group.

    Args:
        src (int): Source rank
        group (ProcessGroup or List[int]): The process group to work on.
        tag (str, optional): A unique identifier for the collective. Default: empty string
    """
    group = _resolve_group(group, tag)
    tensor = torch.ops._c10d_functional.broadcast(
        self, src, _group_or_group_name(group)
    )
    return _maybe_wrap_tensor(tensor)


def broadcast(a: list[int], b: list[int]):
    dimsA = len(a)
    dimsB = len(b)
    ndim = max(dimsA, dimsB)
    expandedSizes: list[int] = []

    for i in range(ndim):
        offset = ndim - 1 - i
        dimA = dimsA - 1 - offset
        dimB = dimsB - 1 - offset
        sizeA = a[dimA] if (dimA >= 0) else 1
        sizeB = b[dimB] if (dimB >= 0) else 1

        if sizeA != sizeB and sizeA != 1 and sizeB != 1:
            # TODO: only assertion error is bound in C++ compilation right now
            raise AssertionError(
                f"The size of tensor a {sizeA} must match the size of tensor b ({sizeB}) at non-singleton dimension {i}"
            )

        expandedSizes.append(sizeB if sizeA == 1 else sizeA)

    return expandedSizes


def broadcast(tensor, devices=None, *, out=None):
    r"""Broadcasts a tensor to specified GPU devices.

    Args:
        tensor (Tensor): tensor to broadcast. Can be on CPU or GPU.
        devices (Iterable[torch.device, str or int], optional): an iterable of
          GPU devices, among which to broadcast.
        out (Sequence[Tensor], optional, keyword-only): the GPU tensors to
          store output results.

    .. note::
        Exactly one of :attr:`devices` and :attr:`out` must be specified.

    Returns:
        - If :attr:`devices` is specified,
            a tuple containing copies of :attr:`tensor`, placed on
            :attr:`devices`.
        - If :attr:`out` is specified,
            a tuple containing :attr:`out` tensors, each containing a copy of
            :attr:`tensor`.
    """
    tensor = _handle_complex(tensor)
    if not ((devices is None) ^ (out is None)):
        raise RuntimeError(
            f"Exactly one of 'devices' and 'out' must be specified, but got devices={devices} and out={out}"
        )
    if devices is not None:
        devices = [_get_device_index(d) for d in devices]
        return torch._C._broadcast(tensor, devices)
    else:
        # pyrefly: ignore [bad-argument-type]
        return torch._C._broadcast_out(tensor, out)


def broadcast(tensor, src, group=group.WORLD):
    """
    Broadcasts the tensor to the whole group.

    ``tensor`` must have the same number of elements in all processes
    participating in the collective.

    Arguments:
        tensor (Tensor): Data to be sent if ``src`` is the rank of current
            process.
        src (int): Source rank.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        Tensor: Received tensor from the broadcast op.

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile(
            "broadcast",
            suggestion="torch.distributed._functional_collectives.broadcast",
        )
    _deprecated("broadcast", "torch.distributed._functional_collectives.broadcast")
    return _Broadcast.apply(src, group, tensor)


def broadcast(result: _ods_ir.Type, src: _ods_ir.Value[_ods_ir.RankedTensorType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BroadcastOp(result=result, src=src, loc=loc, ip=ip).result


def broadcast(operand: _ods_ir.Value[_ods_ir.RankedTensorType], broadcast_sizes: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BroadcastOp(operand=operand, broadcast_sizes=broadcast_sizes, results=results, loc=loc, ip=ip).result


def broadcast(tensor: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BroadcastOp(tensor=tensor, results=results, loc=loc, ip=ip).result


def broadcast(operand: _ods_ir.Value[_ods_ir.RankedTensorType], broadcast_sizes: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return BroadcastOp(operand=operand, broadcast_sizes=broadcast_sizes, results=results, loc=loc, ip=ip).result


def broadcast(vector: _ods_ir.Type, source: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return BroadcastOp(vector=vector, source=source, loc=loc, ip=ip).result


def broadcast(operand, sizes):
  return np.broadcast_to(operand, sizes + np.shape(operand))


def broadcast(prefix_tree: Any, full_tree: Any,
              is_leaf: Callable[[Any], bool] | None = None
              ) -> Any:
  """Broadcasts a tree prefix into the full structure of a given tree.

    Args:
      prefix_tree: a pytree that is a tree prefix of full_tree.
      full_tree: a pytree with the structure to broadcast the prefix leaves into.
      is_leaf: an optionally specified function that will be called at each
        flattening step. It should return a boolean, with true stopping the
        traversal and the whole subtree being treated as a leaf, and false
        indicating the flattening should traverse the current object.

    Returns:
      A pytree matching the structure of full_tree where the leaves of prefix_tree have been
      broadcasted into the leaves of each corresponding subtree.

    Examples:
      >>> import jax
      >>> prefix = (1, 2, 3)
      >>> full = (0, {'a': 0, 'b': 0}, (0, 0))
      >>> jax.tree.broadcast(prefix, full)
      (1, {'a': 2, 'b': 2}, (3, 3))

    See Also:
      - :func:`jax.tree.leaves`
      - :func:`jax.tree.structure`
  """
  return tree_util.tree_broadcast(prefix_tree, full_tree, is_leaf=is_leaf)


def broadcast(x, sz, axis, mesh_axis):
  # Callers of this utility must be in a context where lax is importable.
  from jax import lax  # pyrefly: ignore[missing-module-attribute]
  shape = list(np.shape(x))
  shape.insert(axis, sz)
  broadcast_dims = tuple(np.delete(np.arange(len(shape)), axis))
  x_aval = core.typeof(x)
  if x_aval.sharding.mesh.empty:
    mesh_axis = None
  new_spec = P(*tuple_insert(x_aval.sharding.spec, axis, mesh_axis))
  sharding = x_aval.sharding.update(spec=new_spec)
  # TODO(dougalm, yashkatariya): Delete this context manager once we figure
  # out how to ensure jaxpr arguments always have the context mesh.
  with mesh_lib.use_abstract_mesh(sharding.mesh):
    x, = spmd_names_insert_pvary(lax.broadcast_in_dim(
        x, shape, broadcast_dims, out_sharding=sharding))
    return x


def broadcast(operand: ArrayLike, sizes: Sequence[int], *, out_sharding=None
              ) -> Array:
  """Broadcasts an array, adding new leading dimensions only.

  Args:
    operand: an array
    sizes: a sequence of integers, giving the sizes of new leading dimensions
      to add to the front of the array.

  Returns:
    The result array, of shape ``(*sizes, *operand.shape)`` containing broadcasted
    values of ``operand``.

  See also:
    - :func:`jax.lax.broadcast_in_dim`: general broadcasting at any dimension in the array.
    - :func:`jax.numpy.broadcast_to`: NumPy-style API for general broadcasting.

  Examples:
    >>> import jax.numpy as jnp
    >>> from jax import lax
    >>> arr = jnp.zeros((4, 5))
    >>> result = lax.broadcast(arr, (2, 3))
    >>> result.shape
    (2, 3, 4, 5)
  """
  if len(sizes) == 0 and out_sharding is None:
    return asarray(operand)
  dims = tuple(range(len(sizes), len(sizes) + np.ndim(operand)))
  return broadcast_in_dim(operand, tuple(sizes) + np.shape(operand), dims,
                          out_sharding=out_sharding)

