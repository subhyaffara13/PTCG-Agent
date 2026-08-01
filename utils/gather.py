
def gather(values, index, name="segmented_gather"):
    """
    Gathers from *values* using the index map. For each element in the domain of the index map this operation looks up
    a value for that index in *values*. Two elements from the same segment always get assigned the same value.

    Args:
        values (`torch.Tensor` of shape (B1, ..., Bn, num_segments, V1, ...)):
            Tensor with segment values.
        index (`IndexMap` of shape (B1, ..., Bn, I1, ..., Ik)):
            IndexMap.
        name (`str`, *optional*, defaults to 'segmented_gather'):
            Name for the operation. Currently not used

    Returns:
        `tuple(torch.Tensor)`: Tensor of shape (B1, ..., Bn, I1, ..., Ik, V1, ...) with the gathered values.
    """
    indices = index.indices
    # first, check whether the indices of the index represent scalar values (i.e. not vectorized)
    if len(values.shape[index.batch_dims :]) < 2:
        return torch.gather(
            values,
            index.batch_dims,
            indices.view(
                values.size()[0], -1
            ),  # torch.gather expects index to have the same number of dimensions as values
        ).view(indices.size())
    else:
        # this means we have a vectorized version
        # we have to adjust the index
        indices = indices.unsqueeze(-1).expand(values.shape)
        return torch.gather(values, index.batch_dims, indices)


def gather(
    tensor: torch.Tensor,
    gather_list: list[torch.Tensor] | None = None,
    dst: int | None = None,
    group: ProcessGroup | None = None,
    async_op: bool = False,
    group_dst: int | None = None,
):
    """
    Gathers a list of tensors in a single process.

    This function requires all tensors to be the same size on each process.

    Args:
        tensor (Tensor): Input tensor.
        gather_list (list[Tensor], optional): List of appropriately,
            same-sized tensors to use for gathered data
            (default is None, must be specified on the destination rank)
        dst (int, optional): Destination rank on global process group (regardless of ``group`` argument).
            (If both ``dst`` and ``group_dst`` are None, default is global rank 0)
        group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        async_op (bool, optional): Whether this op should be an async op
        group_dst (int, optional): Destination rank on ``group``.  Invalid to specify both ``dst`` and ``group_dst``

    Returns:
        Async work handle, if async_op is set to True.
        None, if not async_op or if not part of the group

    .. note:: Note that all Tensors in gather_list must have the same size.

    Example::
        >>> # xdoctest: +SKIP("no rank")
        >>> # We have 2 process groups, 2 ranks.
        >>> tensor_size = 2
        >>> device = torch.device(f'cuda:{rank}')
        >>> tensor = torch.ones(tensor_size, device=device) + rank
        >>> if dist.get_rank() == 0:
        >>>     gather_list = [torch.zeros_like(tensor, device=device) for i in range(2)]
        >>> else:
        >>>     gather_list = None
        >>> dist.gather(tensor, gather_list, dst=0)
        >>> # Rank 0 gets gathered data.
        >>> gather_list
        [tensor([1., 1.], device='cuda:0'), tensor([2., 2.], device='cuda:0')] # Rank 0
        None                                                                   # Rank 1

    """
    relevant_args = (tensor,)
    if has_torch_function(relevant_args):
        return handle_torch_function(
            gather,
            relevant_args,
            tensor,
            gather_list=gather_list,
            dst=dst,
            group=group,
            async_op=async_op,
            group_dst=group_dst,
        )

    _check_single_tensor(tensor, "tensor")

    # Parameter ``gather_list`` may be left unspecified on non-dst ranks.
    if gather_list:
        _check_tensor_list(gather_list, "gather_list")
    else:
        gather_list = []
    _ensure_all_tensors_same_dtype(tensor, gather_list)
    group = _group_or_default_group(group)
    if _rank_not_in_group(group):
        _warn_not_in_group("gather")
        return
    if dst is None and group_dst is None:
        dst = 0
    group_dst = _canonicalize_group_rank(group, dst, group_dst, return_global=False)
    my_group_rank = group.rank()
    _validate_output_list_for_rank(my_group_rank, group_dst, gather_list)
    output_tensors = [gather_list] if group_dst == my_group_rank else []
    input_tensors = [tensor]

    opts = GatherOptions()
    opts.rootRank = group_dst
    opts.asyncOp = async_op
    work = group.gather(output_tensors, input_tensors, opts)

    if async_op:
        return work
    elif (
        work is not None
    ):  # Backward compatible with backends that don't sync at CPP level
        work.wait()


def gather(x, dim, index, sparse_grad=False):
    # sparse_grad doesn't affect forward computation,
    # and backward tracing is taken care of by AOT Autograd
    assert isinstance(x, TensorBox)
    if index.get_numel() == 0:
        # Empty index case. Return an empty array with the same shape
        return new_empty(x, index.get_size())

    size = x.get_size()
    offset = len(size) == 0
    dim = _validate_dim(x, dim, offset)

    if offset:
        x = expand(x, [1])
        size = [1]

    x_loader = x.make_loader()
    index_loader = index.make_loader()

    def fn(idx):
        idx = list(idx)
        gather_idx = ops.indirect_indexing(index_loader(idx), size[dim])
        if len(idx) == 0:
            idx = [gather_idx]
        else:
            idx[dim] = gather_idx
        return x_loader(idx)

    return Pointwise.create(
        device=x.get_device(),
        dtype=x.get_dtype(),
        inner_fn=fn,
        ranges=index.get_size(),
    )


def gather(g: jit_utils.GraphContext, self, dim, index, sparse_grad=False):
    if symbolic_helper._maybe_get_const(sparse_grad, "i"):
        return symbolic_helper._unimplemented("gather", "sparse_grad == True")
    return g.op("GatherElements", self, index, axis_i=dim)


def gather(g: jit_utils.GraphContext, self, dim, index, sparse_grad=False):
    if symbolic_helper._maybe_get_const(sparse_grad, "i"):
        return symbolic_helper._unimplemented("gather", "sparse_grad == True", self)
    # NOTE: This workaround is needed since GatherElement is only supported
    #       since opset 11, and Gather in ONNX is not the same as torch.gather.
    scalar_type = _type_utils.JitScalarType.from_value(self)
    values = g.op("Constant", value_t=torch.LongTensor([0, 1]))
    depth = size(g, self, g.op("Constant", value_t=torch.LongTensor([dim])))
    index = g.op(
        "Cast",
        g.op("OneHot", index, depth, values, axis_i=dim),
        to_i=scalar_type.onnx_type(),
    )
    mul = g.op("Mul", symbolic_helper._unsqueeze_helper(g, self, [dim + 1]), index)
    return symbolic_helper._reducesum_helper(g, mul, axes_i=[dim], keepdims_i=0)


def gather(tensors, dim=0, destination=None, *, out=None):
    r"""Gathers tensors from multiple GPU devices.

    Args:
        tensors (Iterable[Tensor]): an iterable of tensors to gather.
          Tensor sizes in all dimensions other than :attr:`dim` have to match.
        dim (int, optional): a dimension along which the tensors will be
          concatenated. Default: ``0``.
        destination (torch.device, str, or int, optional): the output device.
          Can be CPU or CUDA. Default: the current CUDA device.
        out (Tensor, optional, keyword-only): the tensor to store gather result.
          Its sizes must match those of :attr:`tensors`, except for :attr:`dim`,
          where the size must equal ``sum(tensor.size(dim) for tensor in tensors)``.
          Can be on CPU or CUDA.

    .. note::
        :attr:`destination` must not be specified when :attr:`out` is specified.

    Returns:
        - If :attr:`destination` is specified,
            a tensor located on :attr:`destination` device, that is a result of
            concatenating :attr:`tensors` along :attr:`dim`.
        - If :attr:`out` is specified,
            the :attr:`out` tensor, now containing results of concatenating
            :attr:`tensors` along :attr:`dim`.
    """
    tensors = [_handle_complex(t) for t in tensors]
    if out is None:
        if destination == -1:
            warnings.warn(
                "Using -1 to represent CPU tensor is deprecated. Please use a "
                'device object or string instead, e.g., "cpu".',
                FutureWarning,
                stacklevel=2,
            )
        destination = _get_device_index(destination, allow_cpu=True, optional=True)
        return torch._C._gather(tensors, dim, destination)
    else:
        if destination is not None:
            raise RuntimeError(
                f"'destination' must not be specified when 'out' is specified, but got destination={destination}"
            )
        return torch._C._gather_out(tensors, out, dim)


def gather(outputs: Any, target_device: int | torch.device, dim: int = 0) -> Any:
    r"""Gather tensors from different GPUs on a specified device.

    This function is useful for gathering the results of a distributed computation.
    It takes a sequence of objects, one for each GPU, and returns a single object
    on the specified device.

    Args:
        outputs (Any): A sequence of objects (potentially tensors) to gather.
        target_device (Union[int, torch.device]): The device to gather the tensors to.
            Use 'cpu' for CPU to avoid a deprecation warning.
        dim (int, optional): The dimension along which to gather. Default: 0.

    Returns:
        Any: A gathered object (potentially tensor) on the specified device.
    """

    def gather_map(outputs):
        out = outputs[0]
        if isinstance(out, torch.Tensor):
            return Gather.apply(target_device, dim, *outputs)
        if out is None:
            return None
        if isinstance(out, dict):
            if not all(len(out) == len(d) for d in outputs):
                raise ValueError("All dicts must have the same number of keys")
            # pyrefly: ignore [not-callable]
            return type(out)((k, gather_map([d[k] for d in outputs])) for k in out)
        if _is_namedtuple(out):
            # pyrefly: ignore [bad-argument-type]
            return type(out)._make(map(gather_map, zip(*outputs, strict=True)))
        # pyrefly: ignore [bad-argument-type]
        return type(out)(map(gather_map, zip(*outputs, strict=True)))

    # Recursive function calls like this create reference cycles.
    # Setting the function to None clears the refcycle.
    try:
        res = gather_map(outputs)
    finally:
        gather_map = None  # type: ignore[assignment]
    return res


def gather(tensor, dst=0, group=group.WORLD):
    """
    Gathers a list of tensors in a single process.

    Arguments:
        tensor (Tensor): Input tensor.
        dst (int, optional): Destination rank (default is 0).
        group (ProcessGroup, optional): The process group to work on.

    Returns:
        tuple[Tensor]: List of appropriately-sized tensors with the gathered data.
    """
    if torch.compiler.is_compiling():
        _not_supported_under_compile("gather")
    return _Gather.apply(dst, group, tensor)


def gather(src: _ods_ir.Value[_ods_ir.RankedTensorType], indices: _ods_ir.Value[_ods_ir.RankedTensorType], axis: _Union[int, _ods_ir.IntegerAttr], *, efficient_layout: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return GatherOp(src=src, indices=indices, axis=axis, efficient_layout=efficient_layout, results=results, loc=loc, ip=ip).result


def gather(output: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], indices: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], dimension: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return GatherOp(output=output, source=source, indices=indices, dimension=dimension, loc=loc, ip=ip).result


def gather(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _ods_ir.Value[_ods_ir.RankedTensorType], dimension_numbers: _Union[_Any, _ods_ir.Attribute], slice_sizes: _Union[_Union[_Sequence[int], _Buffer], _ods_ir.DenseIntElementsAttr], *, indices_are_sorted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return GatherOp(operand=operand, start_indices=start_indices, dimension_numbers=dimension_numbers, slice_sizes=slice_sizes, indices_are_sorted=indices_are_sorted, results=results, loc=loc, ip=ip).result


def gather(operand: _ods_ir.Value[_ods_ir.RankedTensorType], start_indices: _ods_ir.Value[_ods_ir.RankedTensorType], dimension_numbers: _Union[_Any, _ods_ir.Attribute], slice_sizes: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, indices_are_sorted: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return GatherOp(operand=operand, start_indices=start_indices, dimension_numbers=dimension_numbers, slice_sizes=slice_sizes, indices_are_sorted=indices_are_sorted, results=results, loc=loc, ip=ip).result


def gather(result: _ods_ir.Type, base: _ods_ir.Value, offsets: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], indices: _ods_ir.Value[_ods_ir.VectorType], mask: _ods_ir.Value[_ods_ir.VectorType], pass_thru: _ods_ir.Value[_ods_ir.VectorType], *, alignment: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return GatherOp(result=result, base=base, offsets=offsets, indices=indices, mask=mask, pass_thru=pass_thru, alignment=alignment, loc=loc, ip=ip).result


def gather(operand: ArrayLike, start_indices: ArrayLike,
           dimension_numbers: GatherDimensionNumbers,
           slice_sizes: Shape,
           *,
           unique_indices: bool = False,
           indices_are_sorted: bool = False,
           mode: str | GatherScatterMode | None = None,
           fill_value = None) -> Array:
  """Gather operator.

  Wraps `XLA's Gather operator
  <https://www.openxla.org/xla/operation_semantics#gather>`_.

  :func:`gather` is a low-level operator with complicated semantics, and most JAX
  users will never need to call it directly. Instead, you should prefer using
  `Numpy-style indexing`_, and/or :func:`jax.numpy.ndarray.at`, perhaps in combination
  with :func:`jax.vmap`.

  Args:
    operand: an array from which slices should be taken
    start_indices: the indices at which slices should be taken
    dimension_numbers: a `lax.GatherDimensionNumbers` object that describes
      how dimensions of `operand`, `start_indices` and the output relate.
    slice_sizes: the size of each slice. Must be a sequence of non-negative
      integers with length equal to `ndim(operand)`.
    indices_are_sorted: whether `indices` is known to be sorted. If
      true, may improve performance on some backends.
    unique_indices: whether the elements gathered from ``operand`` are
      guaranteed not to overlap with each other. If ``True``, this may improve
      performance on some backends. JAX does not check this promise: if
      the elements overlap the behavior is undefined.
    mode: how to handle indices that are out of bounds: when set to ``'clip'``,
      indices are clamped so that the slice is within bounds, and when
      set to ``'fill'`` or ``'drop'`` gather returns a slice full of
      ``fill_value`` for the affected slice. The behavior for out-of-bounds
      indices when set to ``'promise_in_bounds'`` is implementation-defined.
    fill_value: the fill value to return for out-of-bounds slices when `mode`
      is ``'fill'``. Ignored otherwise. Defaults to ``NaN`` for inexact types,
      the largest negative value for signed types, the largest positive value
      for unsigned types, and ``True`` for booleans.

  Returns:
    An array containing the gather output.

  Examples:
    As mentioned above, you should basically never use :func:`gather` directly,
    and instead use NumPy-style indexing expressions to gather values from
    arrays.

    For example, here is how you can extract values at particular indices using
    straightforward indexing semantics, which will lower to XLA's Gather operator:

    >>> import jax.numpy as jnp
    >>> x = jnp.array([10, 11, 12])
    >>> indices = jnp.array([0, 1, 1, 2, 2, 2])

    >>> x[indices]
    Array([10, 11, 11, 12, 12, 12], dtype=int32)

    For control over settings like ``indices_are_sorted``, ``unique_indices``, ``mode``,
    and ``fill_value``, you can use the :attr:`jax.numpy.ndarray.at` syntax:

    >>> x.at[indices].get(indices_are_sorted=True, mode="promise_in_bounds")
    Array([10, 11, 11, 12, 12, 12], dtype=int32)

    By comparison, here is the equivalent function call using :func:`gather` directly,
    which is not something typical users should ever need to do:

    >>> from jax import lax
    >>> lax.gather(x, indices[:, None], slice_sizes=(1,),
    ...            dimension_numbers=lax.GatherDimensionNumbers(
    ...                offset_dims=(),
    ...                collapsed_slice_dims=(0,),
    ...                start_index_map=(0,)),
    ...            indices_are_sorted=True,
    ...            mode=lax.GatherScatterMode.PROMISE_IN_BOUNDS)
    Array([10, 11, 11, 12, 12, 12], dtype=int32)

  .. _Numpy-style indexing: https://numpy.org/doc/stable/reference/arrays.indexing.html
  """
  if mode is None:
    mode = GatherScatterMode.PROMISE_IN_BOUNDS
  parsed_mode = GatherScatterMode.from_any(mode)
  if parsed_mode == GatherScatterMode.FILL_OR_DROP:
    if fill_value is None:
      dtype = _dtype(operand)
      if dtypes.issubdtype(dtype, np.inexact):
        fill_value = np.nan
      elif dtypes.issubdtype(dtype, np.signedinteger):
        fill_value = dtypes.iinfo(dtype).min
      elif dtypes.issubdtype(dtype, np.unsignedinteger):
        fill_value = dtypes.iinfo(dtype).max
      elif dtype == dtypes.bool_:
        fill_value = True
      elif dtypes.issubdtype(dtype, dtypes.prng_key):
        fill_value = np.iinfo('uint32').max
      else:
        raise ValueError(f"Unsupported dtype for gather fill_value {dtype}")
  else:
    fill_value = None
  operand, start_indices = core.auto_insert_reshard(operand, start_indices)
  return gather_p.bind(
      operand, start_indices, dimension_numbers=dimension_numbers,
      slice_sizes=core.canonicalize_shape(slice_sizes),
      unique_indices=bool(unique_indices),
      indices_are_sorted=bool(indices_are_sorted),
      mode=parsed_mode,
      fill_value=fill_value)

