import math


def reduce_scatter(x, device_mesh):
    """Reduce-scatter forward, all-gather backward."""
    return _ReduceScatter.apply(x, device_mesh)


def reduce_scatter(
    inputs: Sequence[torch.Tensor],
    outputs: Sequence[torch.Tensor],
    op: int = SUM,
    streams=None,
    comms=None,
) -> None:
    _check_sequence_type(inputs)
    _check_sequence_type(outputs)
    torch._C._nccl_reduce_scatter(inputs, outputs, op, streams, comms)


def reduce_scatter(
    output, input_list, op=ReduceOp.SUM, group=None, async_op: bool = False
):
    """
    Reduces, then scatters a list of tensors to all processes in a group.

    Args:
        output (Tensor): Output tensor.
        input_list (list[Tensor]): List of tensors to reduce and scatter.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op.

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group.

    """
    relevant_args = (output,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            reduce_scatter,
            relevant_args,
            output,
            input_list,
            op=op,
            group=group,
            async_op=async_op,
        )

    _check_single_tensor(output, "output")
    _check_tensor_list(input_list, "input_list")
    _ensure_all_tensors_same_dtype(output, input_list)
    if _rank_not_in_group(group):
        _warn_not_in_group("reduce_scatter")
        return

    opts = ReduceScatterOptions()
    opts.reduceOp = op
    opts.asyncOp = async_op

    group = group or _get_default_group()
    work = group.reduce_scatter([output], [input_list], opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def reduce_scatter(output, input_list, op=ReduceOp.SUM, group=group.WORLD):
    """
    Reduces, then scatters a list of tensors to all processes in a group.

    Arguments:
        output (Tensor): Output tensor.
        input_list (list[Tensor]): List of tensors to reduce and scatter.
        op (optional): One of the values from
            ``torch.distributed.ReduceOp``
            enum.  Specifies an operation used for element-wise reductions.
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        Tensor: Output of the collective.

    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile(
            "reduce_scatter",
            suggestion="torch.distributed._functional_collectives.reduce_scatter_tensor",
        )
    _deprecated(
        "reduce_scatter",
        "torch.distributed._functional_collectives.reduce_scatter_tensor",
    )
    return _Reduce_Scatter.apply(op, group, output, *input_list)


def reduce_scatter(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], scatter_dimension: _Union[int, _ods_ir.IntegerAttr], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, use_global_device_ids: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReduceScatterOp(result=result, operand=operand, scatter_dimension=scatter_dimension, replica_groups=replica_groups, channel_handle=channel_handle, use_global_device_ids=use_global_device_ids, loc=loc, ip=ip).result


def reduce_scatter(tensor: _ods_ir.Value, reduce_scatter_axes: _Union[_Any, _ods_ir.Attribute], out_sharding: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReduceScatterOp(tensor=tensor, reduce_scatter_axes=reduce_scatter_axes, out_sharding=out_sharding, results=results, loc=loc, ip=ip).result


def reduce_scatter(result: _ods_ir.Type, operand: _ods_ir.Value[_ods_ir.RankedTensorType], scatter_dimension: _Union[int, _ods_ir.IntegerAttr], replica_groups: _Union[_Any, _ods_ir.Attribute], *, channel_handle: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, use_global_device_ids: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return ReduceScatterOp(result=result, operand=operand, scatter_dimension=scatter_dimension, replica_groups=replica_groups, channel_handle=channel_handle, use_global_device_ids=use_global_device_ids, loc=loc, ip=ip).result


def reduce_scatter(
    x: jax.Array,
    *,
    axis_name,
    scatter_dimension: int | None = 0,
    reduction: Literal["add", "min", "max", "and", "or", "xor"] = "add",
    num_blocks: int | None = None,
    tile_size: int | None = None,
    vec_size: int | None = None,
) -> jax.Array:
  """Performs a reduce-scatter or all-reduce operation across devices using multimem instructions.

  Args:
    x: Input array. Should be sharded across the specified axis.
    axis_name: Name of the mesh axis to reduce-scatter across.
    scatter_dimension: Axis along which to reduce-scatter. If None, performs
      all-reduce instead. Defaults to 0.
    reduction: Reduction operation to perform. Supported: "add", "min", "max",
      "and", "or", "xor".
    vec_size: Vector size for the layout. If None, automatically inferred from dtype.
    num_blocks: Number of blocks to use. Defaults to the device core count.
    tile_size: Total tile size to split across major, scatter, and minor dimensions.
  """
  num_devices = lax.axis_size(axis_name)
  input_shape = x.shape
  dtype = x.dtype
  ndim = len(input_shape)

  if num_blocks is None:
    num_blocks = backend.get_default_device().core_count

  if scatter_dimension is None:
    major_dims, scatter_dim, minor_dims = 1, math.prod(input_shape), 1
    output_scatter_dim = scatter_dim
    output_shape = input_shape
  else:
    if scatter_dimension < -ndim or scatter_dimension >= ndim:
      raise ValueError(
          f"scatter_dimension {scatter_dimension} out of bounds for array of"
          f" dimension {ndim}"
      )
    if scatter_dimension < 0:
      scatter_dimension += ndim

    scatter_dim = input_shape[scatter_dimension]
    if scatter_dim % num_devices != 0:
      raise ValueError(
          f"Scattered dimension {scatter_dimension} of input ({scatter_dim})"
          f" must be divisible by number of devices ({num_devices})"
      )

    major_dims = math.prod(input_shape[:scatter_dimension])
    minor_dims = math.prod(input_shape[scatter_dimension+1:])
    output_scatter_dim = scatter_dim // num_devices
    output_shape = (
        *input_shape[:scatter_dimension], output_scatter_dim, *input_shape[scatter_dimension + 1 :],
    )

  if (output_size := math.prod(output_shape)) % 128:
    raise ValueError("Output size must be divisible by 128")
  if jnp.issubdtype(dtype, jnp.integer):
    if vec_size is None:
      vec_size = 1  # Integer types only support unvectorized reductions
    elif vec_size != 1:
      raise ValueError("Integer types only support vec_size=1")
  elif vec_size is None:  # vec_size inference for floating point types
    dtype_bits = jnp.finfo(dtype).bits
    max_vec_size = min(128 // dtype_bits, output_size // 128)
    if tile_size is not None:
      max_vec_size_for_tile = tile_size // 128
      max_vec_size = min(max_vec_size, max_vec_size_for_tile)
    vec_size = 32 // dtype_bits  # We don't support ld_reduce below 32-bit
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
    unroll_factor = min(math.prod(output_shape) // min_transfer_elems, 8)
    tile_size = unroll_factor * min_transfer_elems
  if tile_size < min_transfer_elems:
    raise ValueError(
        f"{tile_size=} is smaller than minimum required"
        f" {min_transfer_elems} for {vec_size=}"
    )

  minor_tile = math.gcd(tile_size, minor_dims)
  remaining_tile = tile_size // minor_tile
  scatter_tile = math.gcd(remaining_tile, output_scatter_dim)
  major_tile = remaining_tile // scatter_tile

  if major_dims % major_tile != 0:
    raise NotImplementedError(
        f"Major dimension size ({major_dims}) must be divisible by the"
        f" inferred major tile size ({major_tile}). Consider adjusting tile_size."
    )

  def kernel(x_ref, y_ref, done_barrier):
    dev_idx = lax.axis_index(axis_name)
    x_ref_3d = x_ref.reshape((major_dims, scatter_dim, minor_dims))
    y_ref_3d = y_ref.reshape((major_dims, output_scatter_dim, minor_dims))

    if scatter_dimension is not None:
      dev_slice = pl.ds(dev_idx * output_scatter_dim, output_scatter_dim)
      x_ref_3d = x_ref_3d.at[:, dev_slice, :]

    major_tiles = major_dims // major_tile
    scatter_tiles = output_scatter_dim // scatter_tile
    minor_tiles = minor_dims // minor_tile
    @plgpu.nd_loop((major_tiles, scatter_tiles, minor_tiles), collective_axes="blocks")
    def _transfer_loop(loop_info: plgpu.NDLoopInfo):
      major_tile_idx, scatter_tile_idx, minor_tile_idx = loop_info.index
      idxs = (
          pl.ds(major_tile_idx * major_tile, major_tile),
          pl.ds(scatter_tile_idx * scatter_tile, scatter_tile),
          pl.ds(minor_tile_idx * minor_tile, minor_tile)
      )

      y_ref_3d[idxs] = plgpu.layout_cast(
          plgpu.multimem_load_reduce(
              x_ref_3d.at[idxs], collective_axes=axis_name, reduction_op=reduction
          ),
          plgpu.Layout.WG_STRIDED((major_tile, scatter_tile, minor_tile), vec_size=vec_size)
      )

    # Wait for everyone to finish reading the operands before we exit and potentially free them
    plgpu.semaphore_signal_multicast(done_barrier, collective_axes=axis_name)
    pl.semaphore_wait(done_barrier, num_devices, decrement=False)

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

