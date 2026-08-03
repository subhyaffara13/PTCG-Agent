import functools
from typing import Callable
import math


def all_gather(x, device_mesh):
    """All-gather forward, split backward."""
    return _AllGather.apply(x, device_mesh)


def all_gather(
    inputs: Sequence[torch.Tensor],
    outputs: Sequence[torch.Tensor],
    streams=None,
    comms=None,
) -> None:
    _check_sequence_type(inputs)
    _check_sequence_type(outputs)
    torch._C._nccl_all_gather(inputs, outputs, streams, comms)


def all_gather(
    data_or_fn: T | Callable[[], T],
    stage_name: str | None = None,
    pg: dist.ProcessGroup | None = None,
) -> list[T]:
    """
    A simple all_gather primitive with basic synchronization guard logic,
    by checking payload from all ranks has the same stage name.

    Args:
        data_or_fn: the data to be all gathered across ranks or function to be executed
        stage_name: the sync stage name for out-of-sync protection
        pg: the process group for sync
    Throws:
        RuntimeError from original exception trace
    Returns:
        a list of synced data from all ranks

    Example usage:
    >> all_ids = all_gather(data_or_fn=allocate_id, pg=ext_pg.my_pg)
    """
    payload: T | None = None
    exception: Exception | None = None
    success = True
    # determine if it is an executable function or data payload only
    if callable(data_or_fn):
        try:
            payload = data_or_fn()
        except Exception as e:
            success = False
            exception = e
    else:
        payload = data_or_fn

    sync_obj = SyncPayload(
        stage_name=stage_name,
        success=success,
        payload=payload,
        exception=exception,
    )

    if pg is not None:
        # List of success/failure across all ranks.
        total_list = [None] * dist.get_world_size(pg)
        all_gather_object_enforce_type(pg, total_list, sync_obj)
        # Each rank will throw RuntimeError in case of failure on any rank.
        stage_name = cast(SyncPayload[T], total_list[0]).stage_name
        exception_list: list[tuple[int, Exception]] = []
        ret_list: list[T] = []
        error_msg: str = ""

        for i, sp in enumerate(cast(list[SyncPayload[T]], total_list)):
            if sp.stage_name != stage_name:
                error_msg += (
                    f"Unexpected stage name received from rank {i}: {sp.stage_name} "
                )
                continue
            if not sp.success and sp.exception is not None:
                exception_list.append((i, sp.exception))
                continue
            ret_list.append(sp.payload)

        if len(exception_list) > 0:
            raise RuntimeError(  # type: ignore[misc]
                error_msg,
                exception_list,
            ) from exception_list[0]  # pyrefly: ignore [bad-raise]
        return ret_list
    else:
        if not sync_obj.success:
            raise RuntimeError(
                f"all_gather failed with exception {sync_obj.exception}",
            ) from sync_obj.exception
        return [sync_obj.payload]  # type: ignore[list-item]


def all_gather(tensor_list, tensor, group=None, async_op=False):
    """
    Gathers tensors from the whole group in a list.

    Complex and uneven sized tensors are supported.

    Args:
        tensor_list (list[Tensor]): Output list. It should contain
            correctly-sized tensors to be used for output of the collective.
            Uneven sized tensors are supported.
        tensor (Tensor): Tensor to be broadcast from current process.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    Examples:
        >>> # xdoctest: +SKIP("need process group init")
        >>> # All tensors below are of torch.int64 dtype.
        >>> # We have 2 process groups, 2 ranks.
        >>> device = torch.device(f"cuda:{rank}")
        >>> tensor_list = [
        ...     torch.zeros(2, dtype=torch.int64, device=device) for _ in range(2)
        ... ]
        >>> tensor_list
        [tensor([0, 0], device='cuda:0'), tensor([0, 0], device='cuda:0')] # Rank 0
        [tensor([0, 0], device='cuda:1'), tensor([0, 0], device='cuda:1')] # Rank 1
        >>> tensor = torch.arange(2, dtype=torch.int64, device=device) + 1 + 2 * rank
        >>> tensor
        tensor([1, 2], device='cuda:0') # Rank 0
        tensor([3, 4], device='cuda:1') # Rank 1
        >>> dist.all_gather(tensor_list, tensor)
        >>> tensor_list
        [tensor([1, 2], device='cuda:0'), tensor([3, 4], device='cuda:0')] # Rank 0
        [tensor([1, 2], device='cuda:1'), tensor([3, 4], device='cuda:1')] # Rank 1

        >>> # All tensors below are of torch.cfloat dtype.
        >>> # We have 2 process groups, 2 ranks.
        >>> tensor_list = [
        ...     torch.zeros(2, dtype=torch.cfloat, device=device) for _ in range(2)
        ... ]
        >>> tensor_list
        [tensor([0.+0.j, 0.+0.j], device='cuda:0'), tensor([0.+0.j, 0.+0.j], device='cuda:0')] # Rank 0
        [tensor([0.+0.j, 0.+0.j], device='cuda:1'), tensor([0.+0.j, 0.+0.j], device='cuda:1')] # Rank 1
        >>> tensor = torch.tensor(
        ...     [1 + 1j, 2 + 2j], dtype=torch.cfloat, device=device
        ... ) + 2 * rank * (1 + 1j)
        >>> tensor
        tensor([1.+1.j, 2.+2.j], device='cuda:0') # Rank 0
        tensor([3.+3.j, 4.+4.j], device='cuda:1') # Rank 1
        >>> dist.all_gather(tensor_list, tensor)
        >>> tensor_list
        [tensor([1.+1.j, 2.+2.j], device='cuda:0'), tensor([3.+3.j, 4.+4.j], device='cuda:0')] # Rank 0
        [tensor([1.+1.j, 2.+2.j], device='cuda:1'), tensor([3.+3.j, 4.+4.j], device='cuda:1')] # Rank 1

    """
    # Dynamo has built-in logic to map legacy distributed ops to functional collectives.
    # Let's redirect to a torch function mode that can mimic this logic outside Dynamo
    # (e.g., non-strict export implements such a torch function mode).
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            all_gather,
            relevant_args,
            tensor_list,
            tensor,
            group=group,
            async_op=async_op,
        )

    _check_tensor_list(tensor_list, "tensor_list")
    _check_single_tensor(tensor, "tensor")
    _ensure_all_tensors_same_dtype(tensor_list, tensor)
    if _rank_not_in_group(group):
        _warn_not_in_group("all_gather")
        return

    tensor_list = [
        t if not t.is_complex() else torch.view_as_real(t) for t in tensor_list
    ]
    tensor = tensor if not tensor.is_complex() else torch.view_as_real(tensor)

    group = group or _get_default_group()
    opts = AllgatherOptions()
    opts.asyncOp = async_op
    work = group.allgather([tensor_list], [tensor], opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def all_gather(tensor, group=group.WORLD):
    """
    Gathers tensors from the whole group in a list.

    Arguments:
        tensor (Tensor): Tensor to be broadcast from current process.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        tuple([Tensor]): Output of the collective.

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile(
            "all_gather",
            suggestion="torch.distributed._functional_collectives.all_gather_tensor",
        )
    _deprecated(
        "all_gather", "torch.distributed._functional_collectives.all_gather_tensor"
    )
    return _AllGather.apply(group, tensor)


def all_gather(result: _Sequence[_ods_ir.Type], operands_: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], all_gather_dim: _Union[int, _ods_ir.IntegerAttr], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, use_global_device_ids: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllGatherOp]:
  op = AllGatherOp(result=result, operands_=operands_, all_gather_dim=all_gather_dim, replica_groups=replica_groups, channel_handle=channel_handle, use_global_device_ids=use_global_device_ids, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def all_gather(tensor: _ods_ir.Value, gathering_axes: _Union[_Any, _ods_ir.Attribute], out_sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AllGatherOp(tensor=tensor, gathering_axes=gathering_axes, out_sharding=out_sharding, results=results, loc=loc, ip=ip).result


def all_gather(result: _Sequence[_ods_ir.Type], operands_: _Sequence[_ods_ir.Value[_ods_ir.RankedTensorType]], all_gather_dim: _Union[int, _ods_ir.IntegerAttr], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, use_global_device_ids: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, AllGatherOp]:
  op = AllGatherOp(result=result, operands_=operands_, all_gather_dim=all_gather_dim, replica_groups=replica_groups, channel_handle=channel_handle, use_global_device_ids=use_global_device_ids, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def all_gather(x, axis_name, *, axis_index_groups=None, axis=0, tiled=False,
               to: str = 'varying'):
  """Gather values of x across all replicas.

  If ``x`` is a pytree then the result is equivalent to mapping this function to
  each leaf in the tree.

  This is equivalent to, but faster than, all_to_all(broadcast(x)).

  Args:
    x: array(s) with a mapped axis named ``axis_name``.
    axis_name: hashable Python object used to name a pmapped axis (see the
      :func:`jax.pmap` documentation for more details).
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would run all gather over the first
      two and last two replicas). Groups must cover all axis indices exactly
      once, and all groups must be the same size.
    axis: a positional axis into which the chunks along ``axis_name`` will be
      concatenated.
    tiled: when ``False``, the chunks will be stacked into a fresh positional
      axis at index ``axis`` in the output. When ``True``, ``axis`` has to
      refer to an existing positional dimension and the chunks will be
      concatenated into that dimension.
    to: The output manual axis type, defaults to 'varying'. Valid options are:
      'varying', 'reduced' and 'invarying'.

  Returns:
    Array(s) representing the result of an all-gather along the axis
    ``axis_name``. Shapes are the same as ``x.shape``, but:

    - when ``tiled`` is ``False``, there is a new dimension equal to the
      size of axis ``axis_name`` in position ``axis``,
    - when ``tiled`` is ``True``, the size of dimension in position ``axis``
      is multiplied by the size of axis ``axis_name``.

  For example, with 4 XLA devices available:

  >>> x = np.arange(4)
  >>> y = jax.pmap(lambda x: jax.lax.all_gather(x, 'i'), axis_name='i')(x)
  >>> print(y)
  [[0 1 2 3]
   [0 1 2 3]
   [0 1 2 3]
   [0 1 2 3]]

  An example of using axis_index_groups, groups split by even & odd device ids:

  >>> x = np.arange(16).reshape(4, 4)
  >>> print(x)
    [[ 0  1  2  3]
     [ 4  5  6  7]
     [ 8  9 10 11]
     [12 13 14 15]]
  >>> def f(x):
  ...   return jax.lax.all_gather(
  ...       x, 'i', axis_index_groups=[[0, 2], [3, 1]])
  >>> y = jax.pmap(f, axis_name='i')(x)
  >>> print(y)
  [[[ 0  1  2  3]
    [ 8  9 10 11]]
   [[12 13 14 15]
    [ 4  5  6  7]]
   [[ 0  1  2  3]
    [ 8  9 10 11]]
   [[12 13 14 15]
    [ 4  5  6  7]]]
  """
  return _all_gather_is_async(x, axis_name, axis_index_groups=axis_index_groups,
                              axis=axis, tiled=tiled, to=to, is_async=False)


def all_gather(
    x: jax.Array,
    *,
    axis_name: Hashable,
    gather_dimension: int = 0,
    num_blocks: int | None = None,
    tile_size: int | None = None,
    vec_size: int | None = None,
) -> jax.Array:
  """Performs an all-gather operation using multimem instructions.

  Args:
    x: Input array. Should be sharded across the specified axis.
    axis_name: Name of the mesh axis to all-gather across.
    gather_dimension: Axis along which to gather.
    num_blocks: Number of blocks to use. Defaults to the device core count.
    tile_size: Total tile size to split across major, gather, and minor dimensions.
    vec_size: Vector size for the layout. If None, automatically inferred from dtype.
  """
  num_devices = lax.axis_size(axis_name)
  input_shape = x.shape
  dtype = x.dtype
  ndim = len(input_shape)

  if num_blocks is None:
    num_blocks = backend.get_default_device().core_count

  if gather_dimension < -ndim or gather_dimension >= ndim:
    raise ValueError(
        f"gather_dimension {gather_dimension} out of bounds for array of rank"
        f" {ndim}"
    )
  if gather_dimension < 0:
    gather_dimension += ndim

  input_gather_dim = input_shape[gather_dimension]
  major_dims = math.prod(input_shape[:gather_dimension])
  minor_dims = math.prod(input_shape[gather_dimension+1:])
  output_gather_dim = input_gather_dim * num_devices
  output_shape = (
      *input_shape[:gather_dimension], output_gather_dim, *input_shape[gather_dimension + 1 :],
  )

  if (output_size := math.prod(output_shape)) % 128:
    raise ValueError("Output size must be divisible by 128")
  if jnp.issubdtype(dtype, jnp.integer):
    if vec_size is None:
      vec_size = 1  # Integer types only support unvectorized operations
    elif vec_size != 1:
      raise ValueError("Integer types only support vec_size=1")
  elif vec_size is None:  # vec_size inference for floating point types
    dtype_bits = jnp.finfo(dtype).bits
    max_vec_size = min(128 // dtype_bits, output_size // 128)
    if tile_size is not None:
      max_vec_size_for_tile = tile_size // 128
      max_vec_size = min(max_vec_size, max_vec_size_for_tile)
    vec_size = 32 // dtype_bits  # We don't support multimem below 32-bit
    while vec_size * 2 <= max_vec_size:
      vec_size *= 2
  if math.prod(output_shape) % vec_size:
    raise ValueError(
        "The total number of elements in the output"
        f" ({math.prod(output_shape)}) must be divisible by the vec_size"
        f" ({vec_size})"
    )

  min_transfer_elems = 128 * vec_size
  if tile_size is None:
    # TODO(apaszke): 8 is just an arbitrary unrolling factor. Tune it!
    unroll_factor = min(math.prod(input_shape) // min_transfer_elems, 8)
    tile_size = unroll_factor * min_transfer_elems
  if tile_size < min_transfer_elems:
    raise ValueError(
        f"{tile_size=} is smaller than minimum required"
        f" {min_transfer_elems} for {vec_size=}"
    )

  minor_tile = math.gcd(tile_size, minor_dims)
  remaining_tile = tile_size // minor_tile
  gather_tile = math.gcd(remaining_tile, input_gather_dim)
  major_tile = remaining_tile // gather_tile

  if major_dims % major_tile != 0:
    raise NotImplementedError(
        f"Major dimension size ({major_dims}) must be divisible by the"
        f" inferred major tile size ({major_tile}). Consider adjusting tile_size."
    )

  def kernel(x_ref, y_ref, done_barrier):
    dev_idx = lax.axis_index(axis_name)
    x_ref_3d = x_ref.reshape((major_dims, input_gather_dim, minor_dims))
    y_ref_3d = y_ref.reshape((major_dims, output_gather_dim, minor_dims))
    y_ref_3d = y_ref_3d.at[:, pl.ds(dev_idx * input_gather_dim, input_gather_dim), :]

    major_tiles = major_dims // major_tile
    gather_tiles = input_gather_dim // gather_tile
    minor_tiles = minor_dims // minor_tile
    # TODO(apaszke): Use a TMA pipeline
    @plgpu.nd_loop((major_tiles, gather_tiles, minor_tiles), collective_axes="blocks")
    def _transfer_loop(loop_info: plgpu.NDLoopInfo):
      major_tile_idx, gather_tile_idx, minor_tile_idx = loop_info.index
      idxs = (
          pl.ds(major_tile_idx * major_tile, major_tile),
          pl.ds(gather_tile_idx * gather_tile, gather_tile),
          pl.ds(minor_tile_idx * minor_tile, minor_tile)
      )
      output_data = plgpu.layout_cast(
          x_ref_3d[idxs],
          plgpu.Layout.WG_STRIDED((major_tile, gather_tile, minor_tile), vec_size=vec_size)
      )
      plgpu.multimem_store(output_data, y_ref_3d.at[idxs], axis_name)

    # Wait for everyone to finish storing into our memory before returning.
    plgpu.semaphore_signal_multicast(done_barrier, collective_axes=axis_name)
    pl.semaphore_wait(done_barrier, num_devices, decrement=False)

    # TODO(b/448323639): We fake modify the input to ensure that XLA:GPU copies
    # the operand into symmetric memory.
    @pl.when(dev_idx == -1)
    def _never():
      x_ref[(0,) * len(x_ref.shape)] = jnp.asarray(0, x_ref.dtype)

  compiler_params = plgpu.CompilerParams(
      lowering_semantics=plgpu.LoweringSemantics.Warpgroup
  )
  return plgpu.kernel(
      kernel,
      out_type=jax.ShapeDtypeStruct(output_shape, dtype),
      grid=(num_blocks,),
      grid_names=("blocks",),
      scratch_types=[plgpu.SemaphoreType.REGULAR],
      compiler_params=compiler_params,
  )(x)


def all_gather(x, *, mesh: jax.sharding.Mesh, axis_name: str | Sequence[str],
               memory_space: pltpu.MemorySpace = pltpu.VMEM):
  if isinstance(axis_name, str):
    axis_name = (axis_name,)
  # TODO(sharadmv): enable all gather over multiple axes
  if len(axis_name) > 1:
    raise NotImplementedError("Only one axis supported.")
  axis_name, = axis_name
  if mesh.shape[axis_name] == 1:
    # We can short-circuit here if our axis size is 1
    return x
  def ag_local(x_shard):
    axis_size = lax.axis_size(axis_name)
    out_shape = jax.ShapeDtypeStruct((axis_size, *x_shard.shape), x_shard.dtype)
    out = pl.pallas_call(
        functools.partial(ag_kernel, axis_name=axis_name, mesh=mesh),
        out_shape=out_shape,
        compiler_params=pltpu.CompilerParams(collective_id=0),
        grid_spec=pltpu.PrefetchScalarGridSpec(
            num_scalar_prefetch=0,
            scratch_shapes=(
                (pltpu.SemaphoreType.DMA, pltpu.SemaphoreType.DMA),
                (pltpu.SemaphoreType.DMA, pltpu.SemaphoreType.DMA),
            ),
            in_specs=[pl.BlockSpec(memory_space=memory_space)],
            out_specs=pl.BlockSpec(memory_space=memory_space),
        ),
    )(x_shard)
    return out.reshape((axis_size * x_shard.shape[0], *x_shard.shape[1:]))

  return shard_map.shard_map(
      ag_local, mesh=mesh, in_specs=P(axis_name), out_specs=P(None),
      check_vma=False
  )(x)

